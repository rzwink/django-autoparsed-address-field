from django.test import TestCase

from ..models import Address, Country, State, Locality
from ..services import ScourgifyGeocodingService


class ScourgifyGeocodingServiceTest(TestCase):
    def test_parse_success(self):
        """
        Test the successful parsing of an address using ScourgifyGeocodingService.
        """
        # Use a valid address for Scourgify geocoding
        raw_address = "1600 Pennsylvania Ave NW, Washington, DC 20500"
        with self.settings(ADDRESS_GEOCODER_PROVIDER="scourgify"):
            address = Address(raw=raw_address)

        # Run the service
        service = ScourgifyGeocodingService()
        service.parse(address)

        # Assertions
        self.assertIn("1600", address.address_line_1.upper())
        self.assertIn("WASHINGTON", address.formatted.upper())
        self.assertIsNotNone(address.latitude)
        self.assertIsNotNone(address.longitude)

        # Verify country, state, and locality were created
        country = Country.objects.get(name="USA")
        state = State.objects.get(name="DC", country=country)
        locality = Locality.objects.get(name="WASHINGTON", state=state)

        self.assertIsNotNone(locality)

    def test_parse_failure(self):
        """
        Test the behavior when Scourgify fails to parse an invalid address.
        """
        # Use an invalid address for Scourgify geocoding
        raw_address = "Invalid Address"
        address = Address(raw=raw_address)

        # Run the service and check for errors
        service = ScourgifyGeocodingService()
        service.parse(address)

        # Assertions
        self.assertIsNone(address.address_line_1)
        self.assertIsNone(address.address_line_2)
        self.assertIsNone(address.formatted)
        self.assertIsNone(address.latitude)
        self.assertIsNone(address.longitude)
        self.assertIsNone(address.locality)
