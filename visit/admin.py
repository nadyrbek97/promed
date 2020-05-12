from django.contrib import admin

from .models import Visit, Review, VisitImage
from profiles.models import Doctor


class DoctorListFilter(admin.SimpleListFilter):
    title = 'Выберите Доктора'
    parameter_name = "doctor-id"
    default_value = None

    def lookups(self, request, model_admin):
        list_of_doctors = []
        queryset = Doctor.objects.filter(profile_id__is_superuser=False)
        for doctor in queryset:
            list_of_doctors.append(
                (str(doctor.profile_id.id), doctor.profile_id.full_name)
            )
        return sorted(list_of_doctors, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(doctor_id=self.value())
        return queryset


class VisitImageInline(admin.StackedInline):
    model = VisitImage
    extra = 1


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    inlines = [VisitImageInline, ]
    ordering = ['-start_time']
    date_hierarchy = 'start_time'
    list_display = ['start_time', 'is_finished', 'doctor', 'patient']
    list_filter = ('is_finished', DoctorListFilter, )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    ordering = ['created']
    list_display = ['created', 'is_approved', 'doctor_id', 'patient_id']
