from django.contrib import admin

from .models import (MedicalCenter,
                     MedCenterPhoto,
                     ScheduleTime)


class ScheduleTimeInline(admin.StackedInline):
    model = ScheduleTime
    extra = 1


class MedCenterPhotoInline(admin.StackedInline):
    model = MedCenterPhoto
    extra = 1


@admin.register(MedicalCenter)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ("title", )
    inlines = [ScheduleTimeInline, MedCenterPhotoInline, ]

