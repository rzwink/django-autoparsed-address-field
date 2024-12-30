from django import forms
from django.db import models
from django.db.models import ForeignKey
from django.forms import TextInput

from autoparsed_address_field.descriptors import AddressDescriptor


class AutoParsedAddressField(ForeignKey):
    """
    A custom AddressField that parses raw addresses and populates fields.
    """

    def __init__(self, geocoder_provider=None, **kwargs):
        """
        Initialize the field with optional custom geocoder provider.
        """
        kwargs["to"] = "autoparsed_address_field.Address"
        kwargs["on_delete"] = kwargs.get("on_delete", models.CASCADE)
        super().__init__(**kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        """
        Connects custom behavior to the model class.
        """
        super().contribute_to_class(cls, name, **kwargs)
        setattr(cls, name, AddressDescriptor(self))
