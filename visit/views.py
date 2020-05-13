import datetime

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from profiles.models import Doctor, User, Patient
from visit.models import Visit, Review
from profiles.views import med_center, patient_main_page
from visit.forms import (ReviewForm, AppointmentForm,
                         ConclusionForm)
from visit.utils import render_to_pdf


def create_conclusion(request):
    if request.method == "POST":
        form = ConclusionForm(data=request.POST)
        files = request.FILES.getlist('image')
        url_list = []
        if form.is_valid():
            print("is valid")
            print(files)
            # get doctor from request.user
            user = request.user
            # get image from request
            for image in files:
                print(image.name)
                print(image.size)
                fs = FileSystemStorage()
                image_name = fs.save(image.name, image)
                url_list.append(fs.url(image_name))
                print(url_list)
                # ---save image finished----

            doctor_name_surname = User.objects.get(id=user.id).full_name
            # get data from form
            patient_name_surname = form.cleaned_data["user_name_surname"].full_name
            text = form.cleaned_data["text"]

            # ---------pass data for pfd ------
            data = {
                'med_center': med_center.title,
                'doctor_name': doctor_name_surname,
                'patient_name': patient_name_surname,
                'text': text.split("\n"),
                'images': url_list,
                'today': datetime.date.today(),
            }
            pdf = render_to_pdf('pdf/conclusion.html', data)
            return HttpResponse(pdf, content_type='application/pdf')
        print(form.errors)


def create_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST or None)
        if form.is_valid():
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


def create_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST or None)
        if form.is_valid():
            patient = Patient.objects.get(profile_id=request.user.id)
            patient_phone_number = patient.profile_id.userphonenumber_set.all().first().number
            Visit.objects.create(
                patient_id=patient.profile_id.id,
                doctor_id=form.cleaned_data['doctor_choice'].profile_id.id,
                start_time=form.cleaned_data['start_time'],
                preference=form.cleaned_data['text']
            )
            # Email Sent
            print("Email sent to the DOCTOR and ADMIN")
            admin_user_email = User.objects.get(username='admin').email
            mail_context = {
                'patient_full_name': patient.profile_id.full_name,
                'patient_phone_number': patient_phone_number,
                'date_time': form.cleaned_data['start_time'],
                'patient_preference': form.cleaned_data['text'],
                'doctor_choice': form.cleaned_data['doctor_choice'],
            }
            html_message = render_to_string('pdf/mail_template.html', context=mail_context)
            plain_text_message = strip_tags(html_message)

            send_mail('Test message', plain_text_message,
                      settings.EMAIL_HOST_USER, [admin_user_email, form.cleaned_data['doctor_choice'].profile_id.email],
                      html_message=html_message)
            # success message
            messages.success(request, 'Запись прошла успешно!')
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
        visits = Visit.objects.filter(patient__profile_id=user_id).order_by('-start_time')
    paginator = Paginator(visits, 10)
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

