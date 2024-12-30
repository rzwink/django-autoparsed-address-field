from django import forms
from django.forms import TextInput
from autoparsed_address_field.fields import AutoParsedAddressField


class AutoParsedAddressAdminMixin:
    """
    Admin mixin for handling AutoParsedAddressField in the admin interface.
    Displays a text input when creating a new object and a normal ForeignKey
    dropdown when editing an existing object.
    """

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if isinstance(db_field, AutoParsedAddressField):
            # Determine if the instance is new or being edited
            instance = getattr(request, "instance", None)

            if instance is None:  # New object
                return forms.CharField(
                    required=False,
                    widget=TextInput(attrs={"placeholder": "Enter address here..."}),
                )
            else:  # Existing object
                return super().formfield_for_dbfield(db_field, request, **kwargs)

        # Default behavior for other fields
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        """
        Attach the instance to the request for use in formfield_for_dbfield.
        """
        request.instance = obj
        return super().get_form(request, obj, **kwargs)
