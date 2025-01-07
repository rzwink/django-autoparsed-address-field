import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class Locality(models.Model):
    name = models.CharField(_("Name"), max_length=165)
    postal_code = models.CharField(
        _("Postal Code"), max_length=20, blank=True, null=True
    )
    state = models.ForeignKey(
        "State",
        on_delete=models.CASCADE,
        related_name="localities",
        verbose_name=_("State"),
    )

    class Meta:
        unique_together = ("name", "postal_code", "state")
        verbose_name_plural = _("Localities")

    def __str__(self):
        return f"{self.name}, {self.state}"
