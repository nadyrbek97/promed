from rest_framework.views import APIView
from rest_framework.response import Response

from profiles.models import User


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
