from django.db import models
from django.utils.translation import gettext_lazy as _


class MedicalCenter(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    doctor_default_image = models.ImageField(upload_to="med-center-photos/",
                                             null=True, blank=True)
    patient_default_image = models.ImageField(upload_to="med-center-photos/",
                                              null=True, blank=True)
    insta_link = models.CharField(max_length=800, blank=True, null=True)
    facebook_link = models.CharField(max_length=800, blank=True, null=True)
    youtube_link = models.CharField(max_length=800, blank=True, null=True)

    class Meta:
        verbose_name = _("Medical Center")
        verbose_name_plural = _("Medical Centers")

    def __str__(self):
        return f"{self.title}"


class MedCenterPhoto(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="med-center-photos/")
    is_logo = models.BooleanField(default=False)
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE,
                                       related_name="photos")

    class Meta:
        verbose_name = _("Med-Center Photo")
        verbose_name_plural = _("Med-Center Photos")

    def __str__(self):
        return f"{self.title}"


class ScheduleTime(models.Model):
    med_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE,
                                   related_name="schedule_times")
    title = models.CharField(max_length=30)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    is_weekend = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Schedule Time"
        verbose_name_plural = "Schedule Times"

    def __str__(self):
        return f"{self.title}  start: {self.start_time}  end; {self.end_time}"
