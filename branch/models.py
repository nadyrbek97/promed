from django.db import models
from django.utils.translation import gettext_lazy as _

from med_center.models import MedicalCenter


class Branch(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    address = models.CharField(max_length=500)
    is_main = models.BooleanField(default=False)
    med_center_id = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE,
                                      related_name="branches")

    class Meta:
        verbose_name = _("Branch")
        verbose_name_plural = _("Branches")

    def __str__(self):
        return f"{self.title} {self.address}"


class BranchPhoneNumber(models.Model):
    number = models.CharField(max_length=40)
    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE,
                                  related_name="numbers")

    class Meta:
        verbose_name = _("Branch Number")
        verbose_name_plural = _("Branch Numbers")

    def __str__(self):
        return f"{self.number} => {self.branch_id.title}"
