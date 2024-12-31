import logging

from django.db import models


logger = logging.getLogger(__name__)


class State(models.Model):
    name = models.CharField(max_length=165)
    code = models.CharField(max_length=8, blank=True, null=True)
    country = models.ForeignKey(
        "Country", on_delete=models.CASCADE, related_name="states"
    )

    class Meta:
        unique_together = ("name", "country")
        verbose_name_plural = "States"

    def __str__(self):
        return f"{self.name} ({self.code})"
