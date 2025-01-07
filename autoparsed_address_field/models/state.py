import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class State(models.Model):
    name = models.CharField(_("Name"), max_length=165)
    code = models.CharField(_("Code"), max_length=8, blank=True, null=True)
    country = models.ForeignKey(
        "Country",
        on_delete=models.CASCADE,
        related_name="states",
        verbose_name=_("Country"),
    )

    class Meta:
        unique_together = ("name", "country")
        verbose_name_plural = _("States")

    def __str__(self):
        return f"{self.name} ({self.code})"
