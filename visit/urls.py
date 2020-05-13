from django.urls import path

from visit.views import (user_visit_list, filter_by_date,
                         create_review, create_appointment,
                         create_conclusion)

urlpatterns = [
    path('list/', user_visit_list, name="visit-list-view"),
    path('date-filter/', filter_by_date, name="visit-filter-by-date-view"),
    path('create/review/', create_review, name="create-review-view"),
    path('create/appointment/', create_appointment, name="create-appointment-view"),
    path('create/conclusion/', create_conclusion, name="create-conclusion-view")

]
