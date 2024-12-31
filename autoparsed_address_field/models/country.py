import logging

from django.db import models

logger = logging.getLogger(__name__)


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(
        max_length=3, unique=True
    )  # ISO 3166-1 alpha-2 or alpha-3 codes

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name
