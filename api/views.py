import json

from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from api.serializers import ServiceSerializer

from profiles.models import User
from services.models import Service


class GetServicesByDepartmentId(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        result = {}
        department_id = kwargs.get('department_id')
        services = Service.objects.filter(department_id=department_id)
        serialized_services = ServiceSerializer(services, many=True)
        result['services'] = serialized_services.data
        return Response(data=result)


class VisitsForLastWeekData(APIView):
    authentication_classes = []
    permission_classes = []

    # Number of visits in last week
    def get(self, request, format=None):
        labels = ['21-04-2020', '22-04-2020', '23-04-2020', '24-04-2020', '25-04-2020', '26-04-2020', '27-04-2020']
        default_items = [23, 33, 12, 43, 51, 31, 65]

        data = {
            "labels": labels,
            "default": default_items
        }
        return Response(data)


class VisitsByServiceData(APIView):
    authentication_classes = []
    permission_classes = []

    # Number of visits in last week
    def get(self, request, format=None):
        labels = ['Узи Печени', 'Узи Всех Органов', 'Узи Нижних Конечностей',
                  'Узи селезенки', 'Узи Почек', 'Узи Брюшной Полости']
        default_items = [32, 33, 12, 43, 51, 31]

        data = {
            "labels": labels,
            "default": default_items
        }
        return Response(data)


# def get_doctors_list(request):
#     # id = request.GET.get('id','')
#     result = list(User.objects.filter(role=0, is_superuser=False).values('id', 'full_name'))
#     return HttpResponse(json.dumps(result), content_type="application/json")