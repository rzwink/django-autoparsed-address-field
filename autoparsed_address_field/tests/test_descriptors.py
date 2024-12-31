from autoparsed_address_field.models import Address
from django.test import TestCase
from unittest.mock import MagicMock

from autoparsed_address_field.descriptors import AddressDescriptor


class AddressDescriptorTest(TestCase):
    def setUp(self):
        # Mock the model field
        self.mock_field = MagicMock()
        self.mock_field.attname = "address_id"
        self.mock_field.name = "address"

        # Create the descriptor
        self.descriptor = AddressDescriptor(self.mock_field)

        # Create a mock instance
        class MockInstance:
            pass

        self.mock_instance = MockInstance()

    def test_get_with_valid_address(self):
        # Create an Address instance
        address = Address.objects.create(raw="123 Mock St, Mock City, MO")

        # Simulate the value being set on the model
        setattr(self.mock_instance, self.mock_field.attname, address.pk)

        # Retrieve the value using the descriptor
        result = self.descriptor.__get__(self.mock_instance, None)
        self.assertEqual(result, address)

    def test_get_with_no_address(self):
        # Simulate no value being set on the model
        setattr(self.mock_instance, self.mock_field.attname, None)

        # Retrieve the value using the descriptor
        result = self.descriptor.__get__(self.mock_instance, None)
        self.assertIsNone(result)

    def test_get_with_deleted_address(self):
        # Create and delete an Address instance
        address = Address.objects.create(raw="123 Mock St, Mock City, MO")
        setattr(self.mock_instance, self.mock_field.attname, address.pk)
        address.delete()

        # Retrieve the value using the descriptor
        result = self.descriptor.__get__(self.mock_instance, None)
        self.assertIsNone(result)

    def test_set_with_string(self):
        # Set a raw address string
        self.descriptor.__set__(self.mock_instance, "456 Mock Blvd, Mock Town, MT")

        # Ensure the address is created and the primary key is set
        address = Address.objects.get(raw="456 Mock Blvd, Mock Town, MT")
        self.assertEqual(
            getattr(self.mock_instance, self.mock_field.attname), address.pk
        )

    def test_set_with_address_instance(self):
        # Create an Address instance
        address = Address.objects.create(raw="789 Mock Ave, Mock Village, CA")

        # Set the Address instance
        self.descriptor.__set__(self.mock_instance, address)

        # Ensure the primary key is set on the mock instance
        self.assertEqual(
            getattr(self.mock_instance, self.mock_field.attname), address.pk
        )

    def test_set_with_none(self):
        # Set None
        self.descriptor.__set__(self.mock_instance, None)

        # Ensure the value is None
        self.assertIsNone(getattr(self.mock_instance, self.mock_field.attname))

    def test_set_with_invalid_value(self):
        # Attempt to set an invalid value
        with self.assertRaises(ValueError):
            self.descriptor.__set__(self.mock_instance, 12345)
