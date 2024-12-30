from unittest.mock import MagicMock

from django.core.management import call_command
from django.db import models, connection
from django.test import TestCase

from autoparsed_address_field.fields import ArcGISGeocoder, ScourgifyGeocoder
from autoparsed_address_field.fields import AutoParsedAddressField
from autoparsed_address_field.models import Address


class MockGeocoder:
    def parse(self, address_instance):
        address_instance.formatted = "123 Mock St, Mock City, MO"
        address_instance.latitude = 40.7128
        address_instance.longitude = -74.0060
        address_instance.save = MagicMock()


class AutoParsedAddressFieldTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create a mock geocoder
        class MockGeocoder:
            def parse(self, address_instance):
                address_instance.formatted = "123 Mock St, Mock City, MO"
                address_instance.latitude = 40.7128
                address_instance.longitude = -74.0060
                address_instance.save = MagicMock()

        cls.MockGeocoder = MockGeocoder

        # Dynamically create and register a model with the AutoParsedAddressField
        cls.TestModel = type(
            "TestModel",
            (models.Model,),
            {
                "__module__": "autoparsed_address_field.models",
                "address": AutoParsedAddressField(
                    geocoder_provider=lambda: cls.MockGeocoder()
                ),
            },
        )

        # Disable foreign key checks for SQLite
        if connection.vendor == "sqlite":
            with connection.cursor() as cursor:
                cursor.execute("PRAGMA foreign_keys = OFF;")

        # Run migrations
        call_command("makemigrations", "autoparsed_address_field", verbosity=0)
        call_command("migrate", verbosity=0)

        # Re-enable foreign key checks for SQLite
        if connection.vendor == "sqlite":
            with connection.cursor() as cursor:
                cursor.execute("PRAGMA foreign_keys = ON;")

    def test_parse_address_with_mock_geocoder(self):
        # Create and save the Address instance
        mock_address = Address.objects.create(raw="123 Mock St, Mock City, MO")

        # Create an instance of the test model and assign the saved Address
        test_instance = self.TestModel(address=mock_address)
        test_instance.save()

        # Verify that the address was parsed correctly
        self.assertEqual(test_instance.address.formatted, "123 Mock St, Mock City, MO")
        self.assertEqual(test_instance.address.latitude, 40.7128)
        self.assertEqual(test_instance.address.longitude, -74.0060)

    def test_arcgis_geocoder(self):
        geocoder = ArcGISGeocoder()
        mock_address = Address(raw="1600 Pennsylvania Ave NW, Washington, DC")
        geocoder.parse(mock_address)
        self.assertIsNotNone(mock_address.latitude)
        self.assertIsNotNone(mock_address.longitude)

    def test_scourgify_geocoder(self):
        geocoder = ScourgifyGeocoder()
        mock_address = Address(raw="1600 Pennsylvania Ave NW, Washington, DC")
        geocoder.parse(mock_address)
        self.assertEqual(mock_address.street_number, "1600 PENNSYLVANIA AVE NW")
        self.assertIn("WASHINGTON", mock_address.locality.name)
