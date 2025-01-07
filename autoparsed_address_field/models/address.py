import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from ..services import ArcGISGeocodingService, ScourgifyGeocodingService
from ..signals import address_parsed
from ..utils.uuid import generate_uuid_from_address

UNNAMED_ADDRESS = "Unnamed Address"

logger = logging.getLogger(__name__)


class Address(models.Model):
    address_line_1 = models.CharField(
        _("Address Line 1"), max_length=255, blank=True, null=True
    )
    address_line_2 = models.CharField(
        _("Address Line 2"), max_length=255, blank=True, null=True
    )
    locality = models.ForeignKey(
        "Locality",
        on_delete=models.SET_NULL,
        related_name="addresses",
        blank=True,
        null=True,
        verbose_name=_("Locality"),
    )
    raw = models.TextField(_("Raw Address"), blank=True, null=True)
    formatted = models.TextField(_("Formatted Address"), blank=True, null=True)
    latitude = models.FloatField(_("Latitude"), blank=True, null=True)
    longitude = models.FloatField(_("Longitude"), blank=True, null=True)

    address_id = models.TextField(blank=True, db_index=True)

    class Meta:
        verbose_name_plural = _("Addresses")

    def save(self, *args, skip_parsing=False, **kwargs):
        if not skip_parsing:
            if self.raw:
                try:
                    self.parse_address()
                except Exception as e:
                    logger.error(_("Error parsing address: %s"), e)
        print(str(self))
        if str(self) != UNNAMED_ADDRESS:
            self.address_id = generate_uuid_from_address(self)

        super().save(*args, **kwargs)
        self._send_parsed_signal()

    def parse_address(self):
        geocoding_service = self._get_geocoding_service()
        geocoding_service.parse(self)

    def _send_parsed_signal(self):
        address_parsed.send(
            sender=self.__class__,
            model_name=self._meta.model_name,
            address_instance=self,
        )

    def _get_geocoding_service(self):
        from django.conf import settings

        provider = getattr(settings, "ADDRESS_GEOCODER_PROVIDER", "scourgify")
        if provider == "arcgis":
            return ArcGISGeocodingService()
        elif provider == "scourgify":
            return ScourgifyGeocodingService()
        else:
            raise ValueError(_("Unsupported geocoding provider: %s") % provider)

    def __str__(self):
        return self.formatted if self.formatted else (self.raw or UNNAMED_ADDRESS)
