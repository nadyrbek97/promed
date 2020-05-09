from django.urls import path

from api.views import VisitsByServiceData, VisitsForLastWeekData
from api.views import GetServicesByDepartmentId

urlpatterns = [
    # chart js data
    path('data/visits-by-service/', VisitsByServiceData.as_view(), name="visits-by-service-data-view"),
    path('data/visits-for-last-week/', VisitsForLastWeekData.as_view(), name="visits-for-last-week-data-view"),
    # services
    path('services/list/<int:department_id>/', GetServicesByDepartmentId.as_view(), name="services-by-dep-id-view"),

]
