from django.db import models
from geopy.geocoders import ArcGIS
from scourgify import normalize_address_record
from uszipcode import SearchEngine
import logging

from .signals import address_parsed

logger = logging.getLogger(__name__)


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(
        max_length=3, unique=True
    )  # ISO 3166-1 alpha-2 or alpha-3 codes

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=165)
    code = models.CharField(max_length=8, blank=True, null=True)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="states"
    )

    class Meta:
        unique_together = ("name", "country")
        verbose_name_plural = "States"

    def __str__(self):
        return f"{self.name}, {self.country}"


class Locality(models.Model):
    name = models.CharField(max_length=165)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name="localities"
    )

    class Meta:
        unique_together = ("name", "postal_code", "state")
        verbose_name_plural = "Localities"

    def __str__(self):
        return f"{self.name}, {self.state}"


class Address(models.Model):
    address_line_1 = models.CharField(max_length=255)  # e.g., "123 Main Street"
    address_line_2 = models.CharField(
        max_length=255, blank=True, null=True
    )  # e.g., "Apt 4B"
    locality = models.ForeignKey(
        Locality,
        on_delete=models.SET_NULL,
        related_name="addresses",
        blank=True,
        null=True,
    )
    raw = models.TextField(blank=True, null=True)  # Unprocessed input
    formatted = models.TextField(blank=True, null=True)  # Parsed address output
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Addresses"

    def save(self, *args, **kwargs):
        """
        Override save to parse the raw address before saving.
        """
        if self.raw:
            self.parse_address()
        super().save(*args, **kwargs)

        self._send_parsed_signal()

    def parse_address(self):
        """
        Parses the raw address using the selected geocoding provider.
        """
        from django.conf import settings

        provider = getattr(settings, "ADDRESS_GEOCODER_PROVIDER", "scourgify")

        if provider == "arcgis":
            self._parse_with_arcgis()
        elif provider == "scourgify":
            self._parse_with_scourgify()
        else:
            raise ValueError(f"Unsupported geocoding provider: {provider}")

    def _send_parsed_signal(self):
        """
        Sends the address_parsed signal when parsing is successful.
        """
        logger.info("sending signal")

        address_parsed.send(
            sender=self.__class__,
            model_name=self._meta.model_name,
            address_instance=self,
        )

    def _parse_with_arcgis(self):
        """
        Parses the raw address using ArcGIS geocoder.
        """
        geolocator = ArcGIS()
        result = geolocator.geocode(self.raw, exactly_one=True, out_fields="*")
        if result:
            # Extract and set address components from result.raw
            attributes = result.raw.get("attributes", {})

            self.address_line_1 = attributes.get(
                "StAddr", result.address.split(",")[0]
            ).upper()
            self.address_line_2 = attributes.get(
                "SubAddr", ""
            ).upper()  # Secondary address line, if available
            locality_name = attributes.get("City", "").upper()
            state_name = attributes.get("Region", "").upper()
            state_code = attributes.get("RegionAbbr", "").upper()
            postal_code = attributes.get("Postal", "").upper()
            country_name = attributes.get("CntryName", "USA")
            country_code = attributes.get("Country", "USA")  # ISO code from attributes

            # Construct formatted address
            self.formatted = (
                f"{self.address_line_1 or ''}"
                f"{', ' + (self.address_line_2 or '') if self.address_line_2 else ''}, "
                f"{locality_name or ''}, {state_name or ''} {postal_code or ''}".strip(
                    ", "
                ).upper()
            )

            # Set latitude and longitude from raw location data
            location = result.raw.get("location", {})
            self.latitude = location.get("y", None)
            self.longitude = location.get("x", None)

            # Fetch or create Country object
            country, _ = Country.objects.get_or_create(
                name=country_code, defaults={"code": country_code}
            )

            # Fetch or create State object
            state, _ = State.objects.get_or_create(
                name=state_name, country=country, defaults={"code": state_code}
            )

            # Fetch or create Locality object
            self.locality, _ = Locality.objects.get_or_create(
                name=locality_name, postal_code=postal_code, state=state
            )

    def _parse_with_scourgify(self):
        """
        Parses the raw address using Scourgify and retrieves latitude/longitude using uszipcode.
        """
        parsed = normalize_address_record(self.raw)
        if parsed:
            # Construct formatted address
            self.formatted = (
                f"{parsed.get('address_line_1', '') or ''}"
                f"{', ' + (parsed.get('address_line_2') or '') if parsed.get('address_line_2') else ''}, "
                f"{parsed.get('city', '') or ''}, {parsed.get('state', '') or ''} {parsed.get('postal_code', '') or ''}".strip(
                    ", "
                )
            )

            # Set address fields
            self.address_line_1 = parsed.get("address_line_1", "")
            self.address_line_2 = parsed.get("address_line_2", "")
            locality_name = parsed.get("city", "")
            postal_code = parsed.get("postal_code", "")
            state_name = parsed.get("state", "")

            # Fetch or create Locality, State, and Country objects
            country, _ = Country.objects.get_or_create(name="USA")  # Default to USA
            state, _ = State.objects.get_or_create(name=state_name, country=country)
            self.locality, _ = Locality.objects.get_or_create(
                name=locality_name, postal_code=postal_code, state=state
            )

            # Use uszipcode to fetch latitude and longitude
            if postal_code:
                search = SearchEngine()  # Initialize the search engine
                zipcode = search.by_zipcode(postal_code)
                if zipcode:
                    self.latitude = zipcode.lat
                    self.longitude = zipcode.lng

    def __str__(self):
        """
        Returns a human-readable string representation of the Address instance.
        """
        if self.formatted:
            return self.formatted
        elif self.raw:
            return self.raw
        return "Unnamed Address"
