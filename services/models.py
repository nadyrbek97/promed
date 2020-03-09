from django.db import models
from django.utils.translation import gettext_lazy as _

from departament.models import Departament


class Service(models.Model):
    title = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    department = models.ForeignKey(Departament, on_delete=models.CASCADE,
                                   related_name="services")

    class Meta:
        ordering = ["title"]
        verbose_name = _("Service")
        verbose_name_plural = _("Services")

    def __str__(self):
        return f"{self.title}"
