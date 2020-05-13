import datetime
import json

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator

from profiles.forms import UserLoginForm, ConclusionForm, UserAddPhoneNumberForm, DoctorProfileUpdateForm
from profiles.forms import PatientProfileUpdateForm, PatientCreateForm
from profiles.models import User, Patient, Doctor, UserPhoneNumber
from profiles.utils import generate_password

from med_center.models import MedicalCenter
from visit.models import Visit
from visit.forms import ReviewForm, AppointmentForm

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
            role = user.role
            if role == 0:
                return redirect('profile-main-view')
            else:
                return redirect('patient-main-page')
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


def create_patient(request):

    if request.method == "POST":
        try:
            form = PatientCreateForm(request.POST or None)
            if form.is_valid():
                print(form.cleaned_data['full_name'])
                print(form.cleaned_data['phone_number'])
                print(form.cleaned_data['birth_date'])
                print(form.cleaned_data['address'])
                print(form.cleaned_data['email'])
                # # ----------CREATE PATIENT --------
                amount_of_users = User.objects.all().count() + 1000
                patient_username = 'patient_' + str(amount_of_users)
                password = "patient" + str(generate_password())
                print(patient_username)
                print(password)
                created_user = User.objects.create_user(
                    full_name=form.cleaned_data['full_name'],
                    birth_date=form.cleaned_data['birth_date'],
                    email=form.cleaned_data['email'],
                    username=patient_username,
                    password=password,
                    role=1
                )
                patient = Patient(
                    profile_id=created_user,
                    address=form.cleaned_data['address']
                )
                patient.save()
                # -------- Phone Number -----------
                UserPhoneNumber.objects.create(
                    user=created_user,
                    number=form.cleaned_data['phone_number']
                )
                # ---------------------------------
                messages.success(request, 'Пациент создан успешно!!!')
                return redirect(profile_main_view)
            else:
                messages.error(request, "Неправильно заполнены поля, проверьте формат даты рожднения")
                return redirect(profile_main_view)
        except:
            messages.error(request, "Произошла ошибка на стороне сервера 500 :(")
            return redirect(profile_main_view)


@login_required(login_url="/profiles/login/")
def profile_main_view(request):
    user = request.user

    form = ConclusionForm(request.POST)
    create_patient_form = PatientCreateForm()

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
    # samples
    if user.doctor:
        department_id = user.doctor.department_id
        samples = Sample.objects.filter(department_id=department_id)
    else:
        samples = None

    context = {
        "med_center": med_center,
        "samples": samples,
        "create_patient_form": create_patient_form,
        "form": form
    }

    return render(request, "profiles/doctor-main-page.html", context=context)


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
    # patients = set(patients_list)
    paginator = Paginator(patients_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        # "patients": patients,
        "med_center": med_center,
    }

    return render(request, "profiles/patient-list.html", context=context)


@login_required(login_url="/profiles/login/")
def find_patient_by_full_name(request):
    full_name = request.GET.get('full-name')
    patients_list = Patient.objects.filter(profile_id__full_name__icontains=full_name)
    paginator = Paginator(patients_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "med_center": med_center,
    }

    return render(request, "profiles/patient-list.html", context=context)


@login_required(login_url="/profiles/login/")
def patient_autocomplete_search(request):
    if request.is_ajax():
        query = request.GET.get('term', '')
        # query_set = User.objects.filter(Q(role=1) | Q(full_name__startswith=query))[:5]
        query_set = User.objects.filter(role=1).filter(full_name__icontains=query)[:5]
        results = []
        print(query)
        for qs in query_set:
            results.append(qs.full_name)
        data = json.dumps(results)
        print(results)
    else:
        data = "fail"
    mimetype = "application/json"
    return HttpResponse(data, mimetype)


# Doctor Profile Actions
def doctor_detail_page(request):
    # forms
    phone_form = UserAddPhoneNumberForm()
    profile_update_form = DoctorProfileUpdateForm()

    user = request.user.doctor
    doctor = Doctor.objects.get(profile_id=user)
    phone_numbers = UserPhoneNumber.objects.filter(user=doctor.profile_id)
    context = {
        'phone_form': phone_form,
        'profile_update_form': profile_update_form,
        'med_center': med_center,
        'doctor': doctor,
        'phone_numbers': phone_numbers
    }
    return render(request, 'profiles/doctor-page.html', context=context)


@login_required(login_url="/profiles/login/")
def update_doctor_profile(request):
    user = request.user
    profile = None
    doctor = None
    try:
        profile = User.objects.get(id=user.id)
        doctor = Doctor.objects.get(profile_id=profile)
    except (User.DoesNotExist, Doctor.DoesNotExist):
        print("User not Found")
        messages.error(request, "Пользователь не найден")
        redirect(doctor_detail_page)

    if request.method == "POST":
        form = DoctorProfileUpdateForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            profile.full_name = form.cleaned_data["full_name"]
            profile.save()
            if form.cleaned_data['image'] is not None:
                doctor.image = form.cleaned_data["image"]
                doctor.save()
            else:
                print("IMAGE not chosen")
            messages.success(request, "Профиль обновлен успешно!")
            return redirect(doctor_detail_page)
        print("Sample Form Is Not Valid")
        return redirect(doctor_detail_page)
    return redirect(doctor_detail_page)


@login_required(login_url="/profiles/login/")
def create_profile_phone_number(request):
    user_role = User.objects.get(id=request.user.id).role
    user_id = request.user.id
    if request.method == "POST":
        form = UserAddPhoneNumberForm(request.POST or None)
        if form.is_valid():
            phone_number = UserPhoneNumber.objects.create(user_id=user_id,
                                                          number=form.cleaned_data["number"])
            phone_number.save()
            messages.success(request, "Номер добавлен успешно!")
            if user_role == 0:
                return redirect(doctor_detail_page)
            else:
                return redirect(patient_main_page)
        else:
            messages.error(redirect, "FORM IS INVALID")
            if user_role == 0:
                return redirect(doctor_detail_page)
            else:
                return redirect(patient_main_page)


@login_required(login_url="/profiles/login/")
def profile_phone_number_delete(request, phone_id):
    user_role = User.objects.get(id=request.user.id).role
    try:
        sample = UserPhoneNumber.objects.get(id=phone_id)
    except Sample.DoesNotExist:
        print("Number Not Found")
        if user_role == 0:
            return redirect(doctor_detail_page)
        else:
            return redirect(patient_main_page)
    sample.delete()
    messages.success(request, "Номер удален успешно!")
    if user_role == 0:
        return redirect(doctor_detail_page)
    else:
        return redirect(patient_main_page)


# Patient views
@login_required(login_url="/profiles/login/")
def patient_main_page(request):
    phone_form = UserAddPhoneNumberForm()
    profile_update_form = PatientProfileUpdateForm()
    appointment_form = AppointmentForm()
    user = request.user
    patient = Patient.objects.get(profile_id=user)
    phone_numbers = UserPhoneNumber.objects.filter(user=patient.profile_id)
    review_form = ReviewForm()
    context = {
        'phone_form': phone_form,
        'profile_update_form': profile_update_form,
        'appointment_form': appointment_form,
        'review_form': review_form,
        'med_center': med_center,
        'patient': patient,
        'phone_numbers': phone_numbers
    }
    return render(request, 'profiles/patient-main-page.html', context=context)


@login_required(login_url="/profiles/login/")
def patient_update_profile(request):
    profile = None
    patient = None
    try:
        profile = User.objects.get(id=request.user.id)
        patient = Patient.objects.get(profile_id=profile)
    except (User.DoesNotExist, Patient.DoesNotExist):
        print("User not Found")
        messages.error(request, "Пользователь не найден")
        redirect(patient_main_page)

    if request.method == "POST":
        form = PatientProfileUpdateForm(request.POST or None)
        if form.is_valid():
            profile.full_name = form.cleaned_data["full_name"]
            profile.email = form.cleaned_data["email"]
            patient.address = form.cleaned_data["address"]
            profile.save()
            patient.save()
            messages.success(request, "Профиль обновлен успешно!")
            return redirect(patient_main_page)
        print("Sample Form Is Not Valid")
        return redirect(patient_main_page)
    return redirect(patient_main_page)


