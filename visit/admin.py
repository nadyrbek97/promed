from django.contrib import admin

from .models import Visit
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

    # def value(self):
    #     value = super(DoctorListFilter, self).value()
    #     if value is None:
    #         if self.default_value is None:
    #             all_doctor = Doctor.objects.order_by('profile_id__full_name').first()
    #             value = None if all_doctor is None else all_doctor.profile_id.id
    #             self.default_value = value
    #         else:
    #             value = self.default_value
    #     return str(value)


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    ordering = ['start_time']
    date_hierarchy = 'start_time'
    list_display = ['start_time', 'doctor', 'patient']
    list_filter = ('is_finished', DoctorListFilter, )
