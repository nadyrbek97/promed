from django.db import models

from med_center.models import MedicalCenter


class Departament(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    image = models.ImageField(upload_to='departament/')
    med_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE,
                                   related_name="departaments")

    class Meta:
        verbose_name = "Departament"
        verbose_name_plural = "Departaments"

    def __str__(self):
        return f"{self.title}"

