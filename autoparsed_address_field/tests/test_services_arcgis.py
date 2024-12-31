from django.test import TestCase

from ..models import Address, Country, State, Locality
from ..services import ArcGISGeocodingService


class ArcGISGeocodingServiceTest(TestCase):
    def test_parse_success(self):
        """
        Test the successful parsing of an address using ArcGISGeocodingService.
        """
        # Use a valid address for ArcGIS geocoding
        raw_address = "1600 Pennsylvania Ave NW, Washington, DC 20500, USA"
        with self.settings(ADDRESS_GEOCODER_PROVIDER="arcgis"):
            address = Address(raw=raw_address)

        # Run the service
        service = ArcGISGeocodingService()
        service.parse(address)

        # Assertions
        self.assertIn("1600", address.address_line_1.upper())
        self.assertIn("WASHINGTON", address.formatted.upper())
        self.assertIsNotNone(address.latitude)
        self.assertIsNotNone(address.longitude)

        # Verify country, state, and locality were created
        country = Country.objects.get(name="USA")
        state = State.objects.get(code="DC", country=country)
        locality = Locality.objects.get(name="WASHINGTON", state=state)

        self.assertIsNotNone(locality)

    def test_parse_success_without_country(self):
        """
        Test the successful parsing of an address using ArcGISGeocodingService.
        """
        # Use a valid address for ArcGIS geocoding
        raw_address = "1600 Pennsylvania Ave NW, Washington, DC 20500"
        with self.settings(ADDRESS_GEOCODER_PROVIDER="arcgis"):
            address = Address(raw=raw_address)

        # Run the service
        service = ArcGISGeocodingService()
        service.parse(address)

        # Assertions
        self.assertIn("1600", address.address_line_1.upper())
        self.assertIn("WASHINGTON", address.formatted.upper())
        self.assertIsNotNone(address.latitude)
        self.assertIsNotNone(address.longitude)

        # Verify country, state, and locality were created
        country = Country.objects.get(name="USA")
        state = State.objects.get(code="DC", country=country)
        locality = Locality.objects.get(name="WASHINGTON", state=state)

        self.assertIsNotNone(locality)
