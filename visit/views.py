from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from profiles.models import Doctor, User, Patient
from visit.models import Visit, Review
from profiles.views import med_center, patient_main_page
from visit.forms import ReviewForm


def create_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST or None)
        if form.is_valid():
            print(form.cleaned_data['doctor_choice'])
            print(form.cleaned_data['text'])
            patient = Patient.objects.get(profile_id=request.user.id)
            Review.objects.create(
                doctor_id=form.cleaned_data['doctor_choice'],
                patient_id=patient,
                text=form.cleaned_data['text'],
            )
            messages.success(request, 'Отзыв создан успешно!')
            return redirect(patient_main_page)
        else:
            messages.error(request, 'Form is INVALID')


@login_required(login_url="/profiles/login/")
def user_visit_list(request):
    # Get doctor first
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    # Visits
    visits = []
    if user.role == 0:
        visits = Visit.objects.filter(doctor__profile_id=user_id)
    elif user.role == 1:
        visits = Visit.objects.filter(patient__profile_id=user_id)
    paginator = Paginator(visits, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "med_center": med_center
    }
    if user.role == 0:
        return render(request, "visit/visits-list.html", context=context)
    elif user.role == 1:
        return render(request, "visit/patient-visit-list.html", context=context)


@login_required(login_url="/profiles/login/")
def filter_by_date(request):
    # Get doctor first
    visits = []
    doctor_user_id = request.user.doctor
    doctor = Doctor.objects.get(profile_id=doctor_user_id)
    # Get date filters
    if request.GET.get('date-from') != "" and request.GET.get('date-to') != "":
        if request.GET.get('date-from') is not None:
            date_from = request.GET.get('date-from') + " 00:00:00"
            date_to = request.GET.get('date-to') + " 00:00:00"

            d_from = datetime.strptime(date_from, "%d/%m/%Y %H:%M:%S")
            d_to = datetime.strptime(date_to, "%d/%m/%Y %H:%M:%S")

            print(date_to)
            print(date_from)
            # Visits
            visits = Visit.objects.filter(doctor=doctor)\
                .filter(start_time__range=(d_from, d_to))
            messages.success(request, "Заключения на " + date_from[:8] + " - " + date_to[:8] + " числа.")
    else:
        visits = Visit.objects.filter(doctor=doctor)

    paginator = Paginator(visits, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "med_center": med_center
    }

    return render(request, "visit/visits-list.html", context=context)

