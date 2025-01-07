import unittest
import uuid
from unittest.mock import patch

from django.conf import settings

from autoparsed_address_field.utils.uuid import generate_uuid_from_address


class GenerateUUIDFromAddressTest(unittest.TestCase):
    def setUp(self):
        # Set a test salt in the settings
        self.default_salt = "default-salt"
        settings.ADDRESS_SALT = self.default_salt

    def test_generate_uuid_valid_address(self):
        """Test UUID generation for a valid address."""
        address = "123 Main St, Springfield, USA"
        uuid1 = generate_uuid_from_address(address)
        uuid2 = generate_uuid_from_address(address)

        self.assertEqual(uuid1, uuid2)  # UUID should be consistent
        self.assertTrue(uuid.UUID(uuid1))  # Should produce a valid UUID

    def test_generate_uuid_different_salts(self):
        """Test UUID generation produces different results for different salts."""
        address = "123 Main St, Springfield, USA"

        # Default salt
        uuid1 = generate_uuid_from_address(address)

        # Mock a different salt
        with patch(
            "autoparsed_address_field.utils.uuid.settings.ADDRESS_SALT",
            "different-salt",
        ):
            uuid2 = generate_uuid_from_address(address)

        self.assertNotEqual(uuid1, uuid2)  # UUIDs should differ for different salts

    def test_generate_uuid_different_addresses(self):
        """Test UUID generation produces different results for different addresses."""
        address1 = "123 Main St, Springfield, USA"
        address2 = "456 Elm St, Springfield, USA"

        uuid1 = generate_uuid_from_address(address1)
        uuid2 = generate_uuid_from_address(address2)

        self.assertNotEqual(uuid1, uuid2)  # UUIDs should differ for different addresses

    def test_generate_uuid_empty_address(self):
        """Test UUID generation raises an error for an empty address."""
        with self.assertRaises(ValueError):
            generate_uuid_from_address("")

    def test_generate_uuid_with_default_salt(self):
        """Test UUID generation uses the default salt if settings.ADDRESS_SALT is not set."""
        address = "123 Main St, Springfield, USA"

        # Temporarily unset the ADDRESS_SALT setting
        with patch("autoparsed_address_field.utils.uuid.settings.ADDRESS_SALT", None):
            uuid1 = generate_uuid_from_address(address)

        self.assertEqual(uuid1, "b7baa879-a8ad-dc84-1df4-d6c90aea983a")
