from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from profiles.models import Doctor
from med_center.models import MedicalCenter

from samples.models import Sample
from samples.forms import SampleForm


@login_required(login_url="/profiles/login/")
def sample_list(request):
    # Medical Center
    med_center = MedicalCenter.objects.all()[:1].get()

    form = SampleForm()

    # Get doctor first
    doctor_user_id = request.user.doctor
    doctor = Doctor.objects.get(profile_id=doctor_user_id)
    # Patients
    samples = Sample.objects.filter(department__doctors__exact=doctor)
    context = {
        "form": form,
        "samples": samples,
        "med_center": med_center
    }

    return render(request, "samples/samples-list.html", context=context)


@login_required(login_url="/profiles/login/")
def sample_create(request):

    user = request.user.doctor
    doctor = Doctor.objects.get(profile_id=user)

    if request.method == "POST":
        form = SampleForm(request.POST or None)
        if form.is_valid():
            print(form.cleaned_data['title'])
            print(form.cleaned_data['description'])
            Sample.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                price=500,
                department_id=doctor.department_id.id
            )
            messages.success(request, "Шаблон создан успешно!")
            return redirect(sample_list)
    else:
        messages.error(request, "Произошла ошибка при создании :(")
        form = SampleForm()

    return render(request, "samples/samples-list.html")


@login_required(login_url="/profiles/login/")
@csrf_exempt
def sample_update(request, sample_id):
    try:
        sample = Sample.objects.get(id=sample_id)
    except Sample.DoesNotExist:
        print("Sample Not Found")
        messages.error(request, "Шаблон не найден :(")
        return redirect(sample_list)

    if request.method == "POST":
        form = SampleForm(request.POST or None)
        if form.is_valid():
            sample.title = form.cleaned_data["title"]
            sample.description = form.cleaned_data["description"]
            sample.save()
            messages.success(request, "Шаблон обновлен успешно!")
            return redirect(sample_list)
        print("Sample Form Is Not Valid")
        return redirect(sample_list)
    return redirect(sample_list)


@login_required(login_url="/profiles/login/")
def sample_delete(request, sample_id):
    try:
        sample = Sample.objects.get(id=sample_id)
    except Sample.DoesNotExist:
        print("Sample Not Found")
        return redirect(sample_list)
    sample.delete()
    messages.success(request, "Шаблон удален успешно!")
    return redirect(sample_list)
