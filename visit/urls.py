from django.urls import path

from visit.views import user_visit_list, filter_by_date

urlpatterns = [
    path('list/', user_visit_list, name="visit-list-view"),
    path('date-filter/', filter_by_date, name="visit-filter-by-date-view"),
]
