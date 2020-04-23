from django.urls import path

from samples.views import sample_list, sample_create, sample_update, sample_delete

urlpatterns = [
    path('list/', sample_list, name="sample-list-view"),
    path('create/', sample_create, name="sample-create-view"),
    path('update/<int:sample_id>/', sample_update, name="sample-update-view"),
    path('delete/<int:sample_id>/', sample_delete, name="sample-delete-view"),
]
