import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from profiles.models import (Doctor,
                             Patient)
from services.models import Service


class Visit(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(verbose_name=_("Start date"))
    is_finished = models.BooleanField(verbose_name=_("Finished"), default=False)

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,
                               verbose_name=_("Doctor"), related_name="visits")
    service = models.ManyToManyField(Service, verbose_name=_("Service"),
                                     blank=True,
                                     related_name="visits")
    patient = models.ForeignKey(Patient, verbose_name=_("Patient"),
                                on_delete=models.CASCADE,
                                related_name="visits")
    preference = models.TextField(verbose_name=_("Preference"),
                                  null=True, blank=True)
    text = models.TextField(verbose_name=_("Conclusion Text"),
                            null=True, blank=True)

    class Meta:
        ordering = ['created']
        verbose_name = _("Visit")
        verbose_name_plural = _("Visits")

    def __str__(self):
        return f"Дата: {self.start_time.day}/{self.start_time.month}/{self.start_time.year} " \
               f"Время: {self.start_time.hour}:{self.start_time.minute}." \
               f" Доктор: {self.doctor.profile_id.full_name}"


class VisitImage(models.Model):
    visit_id = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to='visits/' + datetime.datetime.now().strftime("%Y/%m/%d"))
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"visit image {self.uploaded_at}"


class Review(models.Model):
    is_approved = models.BooleanField(verbose_name=_('is_approved'), default=False)
    patient_id = models.ForeignKey(Patient, verbose_name=_('Patient'),
                                   on_delete=models.CASCADE,
                                   related_name='reviews')
    doctor_id = models.ForeignKey(Doctor, verbose_name=_('Doctor'),
                                  on_delete=models.CASCADE,
                                  related_name='reviews', null=True,
                                  blank=True)
    text = models.TextField(verbose_name=_('Text'))
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)

    class Meta:
        ordering = ['created']
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self):
        return f"Отзыв от {self.patient_id.profile_id.full_name} в {self.created}"
