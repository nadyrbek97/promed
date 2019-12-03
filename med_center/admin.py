from django.contrib import admin

from .models import (MedicalCenter,
                     MedCenterPhoto)


admin.site.register(MedicalCenter)
admin.site.register(MedCenterPhoto)
