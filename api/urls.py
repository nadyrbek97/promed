from django.urls import path

from api.views import ( GetServicesByDepartmentId,  VisitsByServiceData,
                        VisitsForLastWeekData, GetDepartmentById)
# from api.views import get_doctors_list

urlpatterns = [
    # chart js data
    path('data/visits-by-service/', VisitsByServiceData.as_view(), name="visits-by-service-data-view"),
    path('data/visits-for-last-week/', VisitsForLastWeekData.as_view(), name="visits-for-last-week-data-view"),
    # services
    path('services/list/<int:department_id>/', GetServicesByDepartmentId.as_view(), name="services-by-dep-id-view"),
    # departments
    path('department/<int:department_id>/', GetDepartmentById.as_view(), name='get-department-view'),
    # doctors
    # path('doctors/list/', get_doctors_list, name='get-doctors-api'),
]
