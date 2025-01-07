import logging

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


logger = logging.getLogger(__name__)


class AutoParsedAddressFieldConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "autoparsed_address_field"
    verbose_name = _("Address Management")

    def ready(self):
        logger.debug("AutoParsedAddressFieldConfig ready")
        from .signals import address_parsed
