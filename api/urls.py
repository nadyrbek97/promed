from django.urls import path

from api.views import VisitsByServiceData, VisitsForLastWeekData
from api.views import GetServicesByDepartmentId
# from api.views import get_doctors_list

urlpatterns = [
    # chart js data
    path('data/visits-by-service/', VisitsByServiceData.as_view(), name="visits-by-service-data-view"),
    path('data/visits-for-last-week/', VisitsForLastWeekData.as_view(), name="visits-for-last-week-data-view"),
    # services
    path('services/list/<int:department_id>/', GetServicesByDepartmentId.as_view(), name="services-by-dep-id-view"),
    # doctors
    # path('doctors/list/', get_doctors_list, name='get-doctors-api'),
]
