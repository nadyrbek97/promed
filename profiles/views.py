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
from profiles.models import User
from profiles.forms import UserLoginForm, ConclusionForm

from samples.models import Sample

from .utils import render_to_pdf


class CreatePDF(View):

    def get(self, request, *args, **kwargs):
        data = {
            'today': datetime.date.today(),
            'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
        }
        pdf = render_to_pdf('pdf/conclusion.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


# def generate_pdf(self, request, *args, **kwargs):
#     data = {
#         'today': datetime.date.today(),
#         'amount': 39.99,
#         'customer_name': 'Cooper Mann',
#         'order_id': 1233434,
#     }
#     pdf = render_to_pdf('pdf/invoice.html', data)
#     # return HttpResponse(pdf, content_type='application/pdf')
#     return HttpResponse(pdf)


def login(request):
    med_center = MedicalCenter.objects.get(id=1)

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
    # med center
    med_center = MedicalCenter.objects.get(id=1)
    user = request.user

    form = ConclusionForm(request.POST)

    if request.method == "POST":
        form = ConclusionForm(data=request.POST)
        if form.is_valid():
            print("is valid")
            user = request.user
            image = request.FILES['image']
            fs = FileSystemStorage()
            name = fs.save(image.name, image)
            url = fs.url(name)
            print(url)

            doctor_name_surname = user.first_name + " " + user.last_name
            patient_name_surname = form.cleaned_data["user_name_surname"]
            amount = 1000
            email = form.cleaned_data["email"]
            text = form.cleaned_data["text"]
            # image = form.cleaned_data["image"]
            # image = form.cleaned_data["image"]
            data = {
                'med_center': med_center.title,
                'doctor_name': doctor_name_surname,
                'patient_name': patient_name_surname,
                'amount': amount,
                'text': text,
                'image': url,
                'today': datetime.date.today(),
            }
            pdf = render_to_pdf('pdf/conclusion.html', data)
            return HttpResponse(pdf, content_type='application/pdf')

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


def patient_list(request):
    # Patients
    patients = User.objects.filter(role=1)

    context = {
        "patients": patients,
    }

    return render(request, "profiles/patient-list.html", context=context)
