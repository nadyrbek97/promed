from rest_framework import serializers

from services.models import Service
from department.models import Department


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        exclude = ['department']


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        exclude = ['med_center']
