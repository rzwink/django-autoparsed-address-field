import logging

from geopy.geocoders import ArcGIS
from ..models import Country, State, Locality

logger = logging.getLogger(__name__)


# Service Classes for Geocoding
class ArcGISGeocodingService:
    def parse(self, address_instance):
        geolocator = ArcGIS()
        result = geolocator.geocode(
            address_instance.raw, exactly_one=True, out_fields="*"
        )

        if not result or ("score" in result.raw and result.raw["score"] < 90):
            logger.error(
                f"ArcGIS could not geocode the address: {address_instance.raw}"
            )
            return

        attributes = result.raw.get("attributes", {})
        self._populate_address_from_attributes(address_instance, attributes, result)

    def _populate_address_from_attributes(self, address_instance, attributes, result):

        address_instance.address_line_1 = attributes.get(
            "StAddr", result.address.split(",")[0]
        ).upper()
        address_instance.address_line_2 = attributes.get("SubAddr", "").upper()
        locality_name = attributes.get("City", "").upper()
        state_name = attributes.get("Region", "").upper()
        state_code = attributes.get("RegionAbbr", "").upper()
        postal_code = attributes.get("Postal", "").upper()
        country_code = attributes.get("Country", "USA")

        address_instance.formatted = (
            f"{address_instance.address_line_1 or ''}"
            f"{', ' + address_instance.address_line_2 if address_instance.address_line_2 else ''}, "
            f"{locality_name or ''}, {state_name or ''} {postal_code or ''}".strip(", ")
        ).upper()

        location = result.raw.get("location", {})
        address_instance.latitude = location.get("y", None)
        address_instance.longitude = location.get("x", None)

        country, _ = Country.objects.get_or_create(
            name=country_code, defaults={"code": country_code}
        )
        state, _ = State.objects.get_or_create(
            name=state_name, country=country, defaults={"code": state_code}
        )
        address_instance.locality, _ = Locality.objects.get_or_create(
            name=locality_name, postal_code=postal_code, state=state
        )
