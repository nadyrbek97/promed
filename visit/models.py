from django.db import models
from django.utils.translation import gettext_lazy as _

from profiles.models import (Doctor,
                             Patient)
from services.models import Service


class Visit(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,
                               related_name="visits")
    service = models.ManyToManyField(Service,
                                     related_name="visits")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,
                                related_name="visits")

    class Meta:
        ordering = ['created']
        verbose_name = _("Visit")
        verbose_name_plural = _("Visits")

    def __str__(self):
        return f"visit at {self.start_time} for doctor {self.doctor.profile_id.full_name}"