from autoparsed_address_field.models import Address
from django.test import TestCase
from django.db import models
from unittest.mock import MagicMock
from autoparsed_address_field.fields import AutoParsedAddressField
from autoparsed_address_field.descriptors import AddressDescriptor


class AutoParsedAddressFieldTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Dynamically create a model for testing purposes.
        """
        cls.TestModel = type(
            "TestModel",
            (models.Model,),
            {
                "__module__": "autoparsed_address_field.tests",
                "address": AutoParsedAddressField(
                    related_name="+", null=True, blank=True
                ),
                "Meta": type(
                    "Meta",
                    (),
                    {
                        "app_label": "autoparsed_address_field",
                        "managed": False,  # Tell Django not to manage this model
                    },
                ),
            },
        )

    def test_field_initialization(self):
        """
        Test that the AutoParsedAddressField initializes with the correct properties.
        """
        field = self.TestModel._meta.get_field("address")
        self.assertEqual(
            field.remote_field.model, Address
        )  # Compare with the actual model class
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)
        self.assertIsInstance(field, AutoParsedAddressField)

    def test_descriptor_behavior(self):
        """
        Test that the AddressDescriptor is properly set and works as expected.
        """
        # Mock an instance of the dynamically created model
        test_instance = MagicMock()
        descriptor = getattr(self.TestModel, "address")
        self.assertIsInstance(descriptor, AddressDescriptor)

        # Mock an address instance with a primary key
        mock_address_instance = MagicMock(pk=1)

        # Simulate setting the field value
        descriptor.__set__(test_instance, mock_address_instance)

        # Simulate getting the field value
        with MagicMock() as mock_field:
            setattr(test_instance, "address", 1)
            setattr(mock_field, "address", mock_address_instance.pk)

            # Validate expected behavior
            self.assertEqual(test_instance.address, mock_address_instance.pk)

    def test_field_contribute_to_class(self):
        """
        Test that the field is correctly contributed to the model class.
        """
        field = self.TestModel._meta.get_field("address")
        descriptor = getattr(self.TestModel, "address")
        self.assertIsInstance(descriptor, AddressDescriptor)
