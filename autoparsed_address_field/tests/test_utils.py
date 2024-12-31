from django.test import TestCase
from autoparsed_address_field.utils import create_address_from_keys


class CreateAddressFromKeysTest(TestCase):
    def setUp(self):
        self.address_data = {
            "address_line_1": "123 Main St",
            "address_line_2": "Apt 4B",
            "locality_name": "Columbus",
            "state_name": "Ohio",
            "postal_code": "43212",
            "country_name": "USA",
            "country_code": "USA",
            "latitude": 40.7128,
            "longitude": -74.0060,
        }

    def test_create_address_skip_parsing(self):
        """
        Test that address creation works correctly with skip_parsing=True.
        """
        address = create_address_from_keys(self.address_data, skip_parsing=True)

        # Assert address fields are correctly populated
        self.assertEqual(address.address_line_1, self.address_data["address_line_1"])
        self.assertEqual(address.address_line_2, self.address_data["address_line_2"])
        self.assertEqual(address.locality.name, self.address_data["locality_name"])
        self.assertEqual(address.locality.state.name, self.address_data["state_name"])
        self.assertEqual(
            address.locality.state.country.name, self.address_data["country_name"]
        )
        self.assertEqual(address.latitude, self.address_data["latitude"])
        self.assertEqual(address.longitude, self.address_data["longitude"])

    def test_create_address_with_parsing(self):
        """
        Test that address creation works correctly with skip_parsing=False.
        """
        with self.settings(ADDRESS_GEOCODER_PROVIDER="scourgify"):
            address = create_address_from_keys(self.address_data, skip_parsing=False)

        # Assert address fields are correctly populated
        self.assertEqual(
            address.address_line_1, self.address_data["address_line_1"].upper()
        )
        self.assertEqual(
            address.address_line_2, self.address_data["address_line_2"].upper()
        )
        self.assertEqual(
            address.locality.name, f'{self.address_data["locality_name"]}'.upper()
        )
        self.assertEqual(address.locality.state.name, "OH")
        self.assertEqual(
            address.locality.state.country.name, self.address_data["country_name"]
        )
        self.assertEqual(address.latitude, 39.99)
        self.assertEqual(address.longitude, -83.04)

        # Assert that parsing logic (if any) did not interfere with manual field population
        self.assertEqual(
            address.formatted,
            f"{self.address_data['address_line_1']}, {self.address_data['address_line_2']}, {self.address_data['locality_name']}, "
            f"OH {self.address_data['postal_code']}".strip().upper(),
        )
