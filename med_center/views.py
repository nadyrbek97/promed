from django.shortcuts import render

from med_center.models import MedicalCenter, MedCenterPhoto
from branch.models import Branch, BranchPhoneNumber
from profiles.models import Doctor, User
from department.models import Department
from services.models import Service


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
    doctors = Doctor.objects.all()

    context = {
        "med_center": med_center,
        "logo": logo,
        "schedules": schedule_times,

        "departments": departments,

        "services": services,

        "main_branch": main_branch,
        "main_branch_number": main_branch_number.number,
        "user_role": user_role,
        "doctors": doctors

    }
    return render(request, "med_center/index.html", context=context)
