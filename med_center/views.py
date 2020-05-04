from django.shortcuts import render, redirect
from django.contrib import messages

from med_center.models import MedicalCenter, MedCenterPhoto
from med_center.forms import AppointmentForm

from branch.models import Branch, BranchPhoneNumber
from profiles.models import Doctor, User
from department.models import Department
from services.models import Service


def appointment_form(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST or None)
        if form.is_valid():
            print(form.cleaned_data['patient_full_name'])
            print(form.cleaned_data['patient_phone_number'])
            print(form.cleaned_data['date_time'])
            print(form.cleaned_data['doctor_choice'])
            print(form.cleaned_data['patient_preference'])
            messages.success(request, "Запись произошла успешно!")
            return redirect(main_page_view)
        print("Appointment Form Is Not Valid")
        print(form.errors)
        messages.error(request, "Произошла ошибка при записи. Проверьте формат даты")
        return redirect(main_page_view)


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
