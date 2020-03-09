from django.db import models
from django.utils.translation import gettext_lazy as _

from med_center.models import MedicalCenter


class Departament(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    image = models.ImageField(upload_to='departament/', help_text="only little icons")
    med_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE,
                                   related_name="departments")

    class Meta:
        verbose_name = _("Departament")
        verbose_name_plural = _("Departments")

    def __str__(self):
        return f"{self.title}"

