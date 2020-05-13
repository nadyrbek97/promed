from django.urls import path
from django.conf.urls import url

from profiles.views import (profile_main_view, create_profile_phone_number,
                            profile_phone_number_delete, login, logout,
                            find_patient_by_full_name, patient_list,
                            patient_autocomplete_search, doctor_detail_page,
                            update_doctor_profile, patient_main_page,
                            patient_update_profile, create_patient)

urlpatterns = [
    path('main/', profile_main_view, name='profile-main-view'),
    path('login/', login, name='login-view'),
    path('logout/', logout, name='logout-view'),
    path('patient/list/', patient_list, name='patient-list-view'),
    path('search/', patient_autocomplete_search, name='patient-autocomplete-search-view'),
    path('find-by-full-name/', find_patient_by_full_name, name='patient-find-by-full-name-view'),
    # doctor profile
    path('doctor-detail/', doctor_detail_page, name='doctor-detail-page-view'),
    path('doctor-detail/update/', update_doctor_profile, name='update-doctor-profile-view'),
    path('create/phone-number/', create_profile_phone_number, name='create-phone-number-view'),
    path('create/patient/', create_patient, name='create-patient-view'),
    path('delete/phone-number/<int:phone_id>/', profile_phone_number_delete, name='delete-phone-number-view'),
    # client profile
    path('patient/main/', patient_main_page, name='patient-main-page'),
    path('patient/update/', patient_update_profile, name='update-patient-profile-view'),
    # path('registration/', profile_main_view, name='profile-main-view'),
]