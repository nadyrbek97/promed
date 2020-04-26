from django.urls import path

from api.views import ChartData

urlpatterns = [
    path('chart/data/', ChartData.as_view(), name="chart-data-view"),
]
