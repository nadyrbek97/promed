from rest_framework.views import APIView
from rest_framework.response import Response

from profiles.models import User


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    # Number of visits in last week
    def get(self, request, format=None):
        users_count = User.objects.all().count()
        labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
        default_items = [users_count, 33, 12, 43, 51, 31]

        data = {
            "labels": labels,
            "default" : default_items
        }
        return Response(data)
