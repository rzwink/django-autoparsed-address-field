import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class Country(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=100,
        unique=True,
    )
    code = models.CharField(
        _("Code"),
        max_length=3,
        unique=True,
        help_text=_("ISO 3166-1 alpha-2 or alpha-3 codes"),
    )

    class Meta:
        verbose_name_plural = _("Countries")

    def __str__(self):
        return self.name
