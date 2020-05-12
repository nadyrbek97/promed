from django.urls import path

from visit.views import (user_visit_list, filter_by_date,
                         create_review, create_appointment,)

urlpatterns = [
    path('list/', user_visit_list, name="visit-list-view"),
    path('date-filter/', filter_by_date, name="visit-filter-by-date-view"),
    path('creaete/review/', create_review, name="create-review-view"),
    path('creaete/appointment/', create_appointment, name="create-appointment-view"),
]
