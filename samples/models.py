
from django.db import models

from departament.models import Departament


class Sample(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    department = models.ForeignKey(Departament, on_delete=models.CASCADE,
                                   related_name="samples")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "Sample"
        verbose_name_plural = "Sample"

    def __str__(self):
        return f"{self.title} {self.price}"

