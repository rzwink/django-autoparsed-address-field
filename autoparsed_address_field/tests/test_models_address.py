from django.test import TestCase
from ..models import Address, Country, State, Locality
from ..services import ArcGISGeocodingService, ScourgifyGeocodingService


class AddressModelTest(TestCase):
    def setUp(self):
        """
        Set up test data for the Address model.
        """
        # Create related models
        self.country = Country.objects.create(name="United States", code="USA")
        self.state = State.objects.create(
            name="California", code="CA", country=self.country
        )
        self.locality = Locality.objects.create(
            name="Los Angeles", postal_code="90001", state=self.state
        )

    def test_save_with_valid_raw_address_arcgis(self):
        """
        Test saving an Address with a valid raw address using ArcGIS.
        """
        raw_address = "1600 Pennsylvania Ave NW, Washington, DC 20500, USA"
        with self.settings(ADDRESS_GEOCODER_PROVIDER="arcgis"):
            address = Address.objects.create(raw=raw_address)

        self.assertIsNotNone(address.formatted)
        self.assertIn("1600", address.address_line_1.upper())
        self.assertIn("WASHINGTON", address.formatted.upper())
        self.assertIsNotNone(address.latitude)
        self.assertIsNotNone(address.longitude)

    def test_save_with_valid_raw_address_scourgify(self):
        """
        Test saving an Address with a valid raw address using Scourgify.
        """
        raw_address = "456 Main St, Anytown, TX 12345, USA"
        with self.settings(ADDRESS_GEOCODER_PROVIDER="scourgify"):
            address = Address.objects.create(raw=raw_address)

        self.assertIsNotNone(address.formatted)
        self.assertIn("456", address.address_line_1.upper())
        self.assertIn("ANYTOWN", address.formatted.upper())
        self.assertIsNotNone(address.latitude)
        self.assertIsNotNone(address.longitude)

    def test_save_with_invalid_raw_address_arcgis(self):
        """
        Test saving an Address with an invalid raw address using ArcGIS.
        """
        raw_address = "Invalid Address"
        with self.settings(ADDRESS_GEOCODER_PROVIDER="arcgis"):
            address = Address.objects.create(raw=raw_address)

        self.assertIsNone(address.formatted)
        self.assertIsNone(address.latitude)
        self.assertIsNone(address.longitude)

    def test_save_with_invalid_raw_address_scourgify(self):
        """
        Test saving an Address with an invalid raw address using Scourgify.
        """
        raw_address = "Invalid Address"
        with self.settings(ADDRESS_GEOCODER_PROVIDER="scourgify"):
            address = Address.objects.create(raw=raw_address)

        self.assertIsNone(address.formatted)
        self.assertIsNone(address.latitude)
        self.assertIsNone(address.longitude)

    def test_str_representation(self):
        """
        Test the string representation of an Address instance.
        """
        address = Address.objects.create(
            raw="123 Main St, Springfield, IL", formatted="123 Main St, Springfield, IL"
        )
        self.assertEqual(str(address), "123 Main St, Springfield, IL".upper())

    def test_str_representation_with_no_formatted_address(self):
        """
        Test the string representation when formatted address is not set.
        """
        address = Address.objects.create(raw="123 Main St, Springfield, IL")
        self.assertEqual(str(address), "123 Main St, Springfield, IL".upper())

    def test_str_representation_with_no_raw_or_formatted_address(self):
        """
        Test the string representation when no raw or formatted address is set.
        """
        address = Address.objects.create()
        self.assertEqual(str(address), "Unnamed Address")

    def test_unsupported_geocoding_provider(self):
        """
        Test that a ValueError is raised for unsupported geocoding providers.
        """
        with self.settings(ADDRESS_GEOCODER_PROVIDER="unsupported_provider"):
            address = Address(raw="123 Mock St, Mock City, MO")
            with self.assertRaises(ValueError) as context:
                address.parse_address()

            self.assertIn("Unsupported geocoding provider", str(context.exception))
