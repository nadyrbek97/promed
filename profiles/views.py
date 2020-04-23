import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.views.generic import View
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from med_center.models import MedicalCenter
from profiles.models import User, Patient, Doctor
from visit.models import Visit
from profiles.forms import UserLoginForm, ConclusionForm

from samples.models import Sample

from .utils import render_to_pdf

# Medical Center
med_center = MedicalCenter.objects.first()


def login(request):

    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('profile-main-view')
        context = {
            "med_center": med_center,
            "form": form
        }
        return render(request, 'profiles/login.html', context=context)
    else:
        form = UserLoginForm(request.POST)
        context = {
            "med_center": med_center,
            "form": form
        }
        return render(request, 'profiles/login.html', context=context)


def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect('main-page')


@login_required(login_url="/profiles/login/")
def profile_main_view(request):
    user = request.user

    form = ConclusionForm(request.POST)

    if request.method == "POST":
        form = ConclusionForm(data=request.POST)
        if form.is_valid():
            print("is valid")
            # get doctor from request.user
            user = request.user
            # get image from request
            image = request.FILES['image']
            print(image.name)
            print(image.size)
            fs = FileSystemStorage()
            image_name = fs.save(image.name, image)
            url = fs.url(image_name)
            print(url)
            # ---save image finished----

            doctor_name_surname = user.first_name + " " + user.last_name
            # get data from form
            patient_name_surname = form.cleaned_data["user_name_surname"]
            email = form.cleaned_data["email"]
            text = form.cleaned_data["text"]

            # # ----------CREATE PATIENT --------
            # amount_of_users = User.objects.all().count() + 1
            # patient_username = 'patient_' + str(amount_of_users)
            # default_password = 'patient123'
            # created_user = User.objects.create_user(
            #     username=patient_username,
            #     password=default_password,
            #     first_name=patient_name_surname,
            #     last_name=patient_name_surname,
            #     role=1
            # )
            # Patient.objects.create(profile_id=created_user)
            # print(patient_username)
            # print(amount_of_users)
            # ---------------------------------
            # ---------pass data for pfd ------

            data = {
                'med_center': med_center.title,
                'doctor_name': doctor_name_surname,
                'patient_name': patient_name_surname,
                'text': text,
                'image': url,
                'today': datetime.date.today(),
            }
            pdf = render_to_pdf('pdf/conclusion.html', data)
            return HttpResponse(pdf, content_type='application/pdf')
        print(form.errors)
    # samples
    if user.doctor:
        department_id = user.doctor.department_id
        samples = Sample.objects.filter(department_id=department_id)
    else:
        samples = None

    context = {
        "med_center": med_center,
        "samples": samples,
        "form": form
    }

    return render(request, "profiles/profile-main-page.html", context=context)


@login_required(login_url="/profiles/login/")
def patient_list(request):
    # Get doctor first
    doctor = request.user.doctor

    # Patients
    visits = Visit.objects.filter(doctor=doctor)
    patients_list = []
    for visit in visits:
        patient = Patient.objects.get(visits=visit.id)
        patients_list.append(patient)
    patients = set(patients_list)
    context = {
        "patients": patients,
        "med_center": med_center
    }

    return render(request, "profiles/patient-list.html", context=context)


@login_required(login_url="/profiles/login/")
def visit_list(request):
    # Get doctor first
    doctor_user_id = request.user.doctor
    doctor = Doctor.objects.get(profile_id=doctor_user_id)
    # Patients
    visits = Visit.objects.filter(doctor=doctor)
    context = {
        "visits": visits,
        "med_center": med_center
    }
    visit3 = Visit()

    return render(request, "profiles/visits-list.html", context=context)

