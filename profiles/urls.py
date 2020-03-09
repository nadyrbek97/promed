from django.urls import path, include

from profiles.views import profile_main_view
from profiles.views import login, logout
from profiles.views import patient_list, visit_list, sample_list

urlpatterns = [
    path('main/', profile_main_view, name='profile-main-view'),
    path('login/', login, name='login-view'),
    path('logout/', logout, name='logout-view'),
    path('patient/list/', patient_list, name='patient-list-view'),
    path('visit/list/', visit_list, name='visit-list-view'),
    path('sample/list/', sample_list, name='sample-list-view')
    # path('registration/', profile_main_view, name='profile-main-view'),
]