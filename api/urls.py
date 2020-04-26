from django.urls import path

from api.views import VisitsByServiceData, VisitsForLastWeekData

urlpatterns = [
    path('data/visits-by-service/', VisitsByServiceData.as_view(), name="visits-by-service-data-view"),
    path('data/visits-for-last-week/', VisitsForLastWeekData.as_view(), name="visits-for-last-week-data-view"),
]
