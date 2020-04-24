from django.urls import path
from django.conf.urls import url

from profiles.views import profile_main_view
from profiles.views import login, logout, find_patient_by_full_name
from profiles.views import patient_list, visit_list, patient_autocomplete_search

urlpatterns = [
    path('main/', profile_main_view, name='profile-main-view'),
    path('login/', login, name='login-view'),
    path('logout/', logout, name='logout-view'),
    path('patient/list/', patient_list, name='patient-list-view'),
    path('visit/list/', visit_list, name='visit-list-view'),
    path('search/', patient_autocomplete_search, name='patient-autocomplete-search-view'),
    path('find-by-full-name/', find_patient_by_full_name, name='patient-find-by-full-name-view')

    # path('registration/', profile_main_view, name='profile-main-view'),
]