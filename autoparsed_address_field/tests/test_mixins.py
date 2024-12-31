from unittest.mock import MagicMock, patch
from django import forms
from django.contrib import admin
from django.test import TestCase
from autoparsed_address_field.fields import AutoParsedAddressField
from autoparsed_address_field.mixins import AutoParsedAddressAdminMixin
from autoparsed_address_field.models import Address


class MockModelAdmin(AutoParsedAddressAdminMixin, admin.ModelAdmin):
    """
    A mock ModelAdmin class that includes the AutoParsedAddressAdminMixin for testing.
    """

    pass


class AutoParsedAddressAdminMixinTest(TestCase):
    def setUp(self):
        # Create a mock request object
        self.mock_request = MagicMock()
        self.mock_request.instance = None

        # Set up a mock db_field
        self.db_field = MagicMock(spec=AutoParsedAddressField)
        self.db_field.name = "address"

        # Initialize the admin class
        self.admin = MockModelAdmin(Address, admin.site)

    @patch("autoparsed_address_field.mixins.TextInput")
    def test_formfield_for_new_object(self, mock_text_input):
        """
        Test formfield behavior for new objects.
        """
        # Ensure the instance is None (new object)
        self.mock_request.instance = None

        # Call the method
        formfield = self.admin.formfield_for_dbfield(self.db_field, self.mock_request)

        # Assert the formfield is a CharField with the correct widget
        self.assertIsInstance(formfield, forms.CharField)
        self.assertEqual(formfield.widget, mock_text_input.return_value)
        mock_text_input.assert_called_once_with(
            attrs={"placeholder": "Enter address here..."}
        )

    def test_formfield_for_existing_object(self):
        """
        Test formfield behavior for existing objects.
        """
        # Set an existing instance
        self.mock_request.instance = MagicMock()

        # Call the method
        with patch.object(
            admin.ModelAdmin, "formfield_for_dbfield"
        ) as mock_super_formfield:
            self.admin.formfield_for_dbfield(self.db_field, self.mock_request)
            mock_super_formfield.assert_called_once_with(
                self.db_field, self.mock_request
            )

    def test_formfield_for_non_autoparsed_field(self):
        """
        Test formfield behavior for non-AutoParsedAddressField fields.
        """
        # Use a non-AutoParsedAddressField field
        non_autoparsed_field = MagicMock()

        # Call the method
        with patch.object(
            admin.ModelAdmin, "formfield_for_dbfield"
        ) as mock_super_formfield:
            self.admin.formfield_for_dbfield(non_autoparsed_field, self.mock_request)
            mock_super_formfield.assert_called_once_with(
                non_autoparsed_field, self.mock_request
            )
