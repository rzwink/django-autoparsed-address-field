import logging

from .models import Address

logger = logging.getLogger(__name__)


class AddressDescriptor:
    """
    Custom descriptor to handle assignment of raw addresses to the field.
    Adds protection against infinite recursion and robust handling for `__get__`.
    """

    def __init__(self, field):
        self.field = field

    def __get__(self, instance, owner):
        if instance is None:
            return self

        # Safely attempt to retrieve the attribute, handle AttributeError
        try:
            value = getattr(instance, self.field.attname, None)
            if value:
                # Retrieve the related Address instance if the value is a primary key
                return Address.objects.get(pk=value)
            return None
        except AttributeError as e:
            # Log the error for debugging purposes
            logger.error(f"Error in AddressDescriptor __get__: {e}")
            return None
        except Address.DoesNotExist:
            # Handle the case where the Address object is deleted but the reference remains
            return None

    def __set__(self, instance, value):
        # Prevent infinite recursion with a guard
        if hasattr(instance, "_address_guard"):
            return

        try:
            # Set guard to prevent re-entrant calls
            setattr(instance, "_address_guard", True)

            if isinstance(value, str):
                address_instance, _ = Address.objects.get_or_create(raw=value)
                setattr(instance, self.field.attname, address_instance.pk)
            elif isinstance(value, Address):
                setattr(instance, self.field.attname, value.pk)
            elif value is None:
                setattr(instance, self.field.attname, None)
            else:
                raise ValueError(
                    f"{self.field.name} must be a raw address string or an Address instance."
                )
        finally:
            # Clean up the guard
            delattr(instance, "_address_guard")
