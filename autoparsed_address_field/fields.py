from django.db import models
from autoparsed_address_field.descriptors import AddressDescriptor


class AutoParsedAddressField(models.ForeignKey):
    """
    A custom ForeignKey that integrates with autoparsed address fields.
    """

    def __init__(self, foreign_key_class=models.ForeignKey, **kwargs):
        """
        Initialize the custom ForeignKey.
        """
        self.foreign_key_class = foreign_key_class
        kwargs["to"] = "autoparsed_address_field.Address"
        kwargs["on_delete"] = kwargs.get("on_delete", models.CASCADE)
        super().__init__(**kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        """
        Adds custom behavior to the model class.
        """
        super().contribute_to_class(cls, name, **kwargs)
        setattr(cls, name, AddressDescriptor(self))
