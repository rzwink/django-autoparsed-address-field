from django.apps import AppConfig


class AutoParsedAddressFieldConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "autoparsed_address_field"
    verbose_name = "Address Management"
