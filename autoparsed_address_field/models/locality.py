import logging

from django.db import models

logger = logging.getLogger(__name__)


class Locality(models.Model):
    name = models.CharField(max_length=165)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    state = models.ForeignKey(
        "State", on_delete=models.CASCADE, related_name="localities"
    )

    class Meta:
        unique_together = ("name", "postal_code", "state")
        verbose_name_plural = "Localities"

    def __str__(self):
        return f"{self.name}, {self.state}"
