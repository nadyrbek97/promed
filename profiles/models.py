from django.db import models
from django.contrib.auth.models import AbstractUser

from profiles.choices import ROLE, GENDER


class User(AbstractUser):
    username = models.CharField(max_length=200, unique=True)
    role = models.PositiveSmallIntegerField(choices=ROLE, default=0)
    gender = models.PositiveSmallIntegerField(choices=GENDER, default=1)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField("Email", max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.role}: {self.first_name} {self.last_name}"


class Doctor(models.Model):
    profile_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    experience = models.IntegerField(default=1)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

    def __str__(self):
        return f"{self.profile_id.first_name} {self.profile_id.last_name}"


class UserPhoneNumber(models.Model):
    number = models.CharField(max_length=40)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Patient(models.Model):
    profile_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def __str__(self):
        return f"{self.profile_id.first_name} {self.profile_id.last_name}"
