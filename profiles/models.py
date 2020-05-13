from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, post_delete
from django.utils.translation import gettext_lazy as _


from profiles.choices import ROLE, GENDER

from department.models import Department


class User(AbstractUser):
    username = models.CharField(max_length=200, unique=True)
    role = models.PositiveSmallIntegerField(choices=ROLE, default=0)
    gender = models.PositiveSmallIntegerField(choices=GENDER, default=1)
    full_name = models.CharField(max_length=150)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField("Email", max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.full_name} {self.birth_date}"


class Doctor(models.Model):
    profile_id = models.OneToOneField(User,
                                      on_delete=models.CASCADE,
                                      primary_key=True)
    department_id = models.ForeignKey(Department,
                                      null=True, blank=True,
                                      on_delete=models.CASCADE,
                                      related_name="doctors")
    experience = models.IntegerField(default=1)
    salary = models.DecimalField(max_digits=10, decimal_places=2,
                                 null=True, blank=True)
    image = models.ImageField(upload_to="doctors/",
                              null=True, blank=True)

    class Meta:
        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors")

    def __str__(self):
        return f"{self.profile_id.full_name} ({self.department_id})"


class UserPhoneNumber(models.Model):
    number = models.CharField(max_length=40)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Patient(models.Model):
    profile_id = models.OneToOneField(User, on_delete=models.CASCADE,
                                      primary_key=True,
                                      verbose_name=_("Profile"))
    address = models.CharField(null=True, blank=True,
                               max_length=255, verbose_name=_("Address"))
    first_password = models.CharField(null=True, blank=True,
                                      max_length=255, verbose_name=_("Initial Password"))

    class Meta:
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")

    def __str__(self):
        return f"{self.profile_id.full_name}"


# function to create doctor or patient after creating User
def create_doctor_or_patient(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        if user.role == 0:
            Doctor.objects.create(profile_id=user)
        elif user.role == 1:
            Patient.objects.create(profile_id=user)


post_save.connect(create_doctor_or_patient, sender=User)

