import logging

from django.db import models

from ..signals import address_parsed
from ..services import ArcGISGeocodingService, ScourgifyGeocodingService

logger = logging.getLogger(__name__)


class Address(models.Model):
    address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    locality = models.ForeignKey(
        "Locality",
        on_delete=models.SET_NULL,
        related_name="addresses",
        blank=True,
        null=True,
    )
    raw = models.TextField(blank=True, null=True)  # Unprocessed input
    formatted = models.TextField(blank=True, null=True)  # Parsed address output
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Addresses"

    def save(self, *args, skip_parsing=False, **kwargs):
        if not skip_parsing:
            if self.raw:
                try:
                    self.parse_address()
                except Exception as e:
                    logger.error(f"Error parsing address: {e}")
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
            raise ValueError(f"Unsupported geocoding provider: {provider}")

    def __str__(self):
        return self.formatted if self.formatted else (self.raw or "Unnamed Address")
