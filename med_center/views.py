from django.shortcuts import render

from med_center.models import MedicalCenter, MedCenterPhoto
from branch.models import Branch, BranchPhoneNumber
from profiles.models import Doctor


def main_page_view(request):

    # med center
    med_center = MedicalCenter.objects.get(id=1)
    logo = med_center.photos.filter(is_logo=True).first()
    schedule_times = med_center.schedule_times.all()

    main_branch = Branch.objects.get(med_center_id=med_center.id)
    main_branch_number = main_branch.numbers.first()
    doctors = Doctor.objects.all()

    context = {
        "med_center": med_center,
        "logo": logo,
        "schedules": schedule_times,

        "main_branch": main_branch,
        "main_branch_number": main_branch_number.number,
        "doctors": doctors

    }
    return render(request, "med_center/index.html", context=context)
