from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from med_center.models import MedicalCenter, MedCenterPhoto
from med_center.forms import AppointmentForm

from branch.models import Branch, BranchPhoneNumber
from profiles.models import Doctor, User
from profiles.views import med_center
from department.models import Department
from services.models import Service


def appointment_form(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST or None)
        if form.is_valid():
            print("Email sent")
            admin_user_email = User.objects.get(username='admin').email
            mail_context = {
                'patient_full_name': form.cleaned_data['patient_full_name'],
                'patient_phone_number': form.cleaned_data['patient_phone_number'],
                'date_time': form.cleaned_data['date_time'],
                'patient_preference': form.cleaned_data['patient_preference'],
                'doctor_choice': form.cleaned_data['doctor_choice'],
            }
            html_message = render_to_string('pdf/mail_template.html', context=mail_context)
            plain_text_message = strip_tags(html_message)

            send_mail('Test message', plain_text_message,
                      settings.EMAIL_HOST_USER, [admin_user_email, ],
                      html_message=html_message)
            messages.success(request, "Запись произошла успешно!")
            return redirect(main_page_view)
        print("Appointment Form Is Not Valid")
        print(form.errors)
        messages.error(request, "Произошла ошибка при записи. Проверьте формат даты")
        return redirect(main_page_view)


def about_page(request):
    # branch
    main_branch = Branch.objects.get(med_center_id=med_center.id)
    main_branch_number = main_branch.numbers.first()

    logo = med_center.photos.filter(is_logo=True).first()

    context = {
        "med_center": med_center,
        "main_branch_number": main_branch_number.number,
        "logo": logo
    }

    return render(request, 'med_center/about.html', context=context)


def departments_page(request):
    # branch
    main_branch = Branch.objects.get(med_center_id=med_center.id)
    main_branch_number = main_branch.numbers.first()

    logo = med_center.photos.filter(is_logo=True).first()
    departments = Department.objects.all()

    context = {
        "med_center": med_center,
        "main_branch_number": main_branch_number.number,
        "logo": logo,
        "departments": departments
    }

    return render(request, 'med_center/departments.html', context=context)


def main_page_view(request):
    # user info
    user_role = None
    if request.user.is_authenticated:
        user_role = User.objects.get(id=request.user.id).role

    # med center
    med_center = MedicalCenter.objects.get(title="Forever Med")
    logo = med_center.photos.filter(is_logo=True).first()
    schedule_times = med_center.schedule_times.all()

    # departments
    departments = Department.objects.all()

    # services
    services = Service.objects.filter(department_id=1)

    # branch
    main_branch = Branch.objects.get(med_center_id=med_center.id)
    main_branch_number = main_branch.numbers.first()

    # doctors
    doctors = Doctor.objects.filter(profile_id__is_superuser=False)

    # form
    form = AppointmentForm()

    context = {
        "med_center": med_center,
        "logo": logo,
        "schedules": schedule_times,
        "departments": departments,
        "services": services,
        "main_branch": main_branch,
        "main_branch_number": main_branch_number.number,
        "user_role": user_role,
        "doctors": doctors,
        "form": form
    }
    return render(request, "med_center/index.html", context=context)
