from django.db import models


class MedicalCenter(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name = "Medical Center"
        verbose_name_plural = "Medical Centers"

    def __str__(self):
        return f"{self.title}"


class MedCenterPhoto(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="med-center-photos/")
    is_logo = models.BooleanField(default=False)
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE,
                                       related_name="photos")

    class Meta:
        verbose_name = "Med-Center Photo"
        verbose_name_plural = "Med-Center Photos"

    def __str__(self):
        return f"{self.title}"
