from django import forms
from django.forms import ValidationError

from django_select2 import forms as s2_forms

from profiles.models import Doctor, User


class ConclusionForm(forms.Form):
    user_name_surname = forms.ModelChoiceField(
        queryset=User.objects.filter(role=1),
        label="Ф.И.О пациента",
        widget=s2_forms.ModelSelect2Widget(
            queryset=User.objects.filter(role=1),
            search_fields=["full_name__icontains", 'username__icontains'],
            attrs={'data-placeholder': 'ф.и.о пациента ...', 'class': 'form-control'}
        )
    )
    text = forms.CharField(
        label="Текст заключения",
        widget=forms.Textarea(
            attrs={
                'width': "100%", 'cols': "100", 'rows': "20",
                'placeholder': 'Текст заключения',
                'class': 'form-control',
                'id': 'conclusion-text'}))
    image = forms.FileField(
        required=False,
        label="Выберите снимок",
        widget=forms.FileInput(
            attrs={
                'name': 'image',
                'placeholder': 'Выберите снимок',
                'class': 'custom-file-input',
                'multiple': 'true',
                'id': 'image-input-file'
            }))

    # def clean_user_name_surname(self):
    #     user_name_surname = self.cleaned_data['user_name_surname']
    #     if len(user_name_surname) < 5:
    #         raise ValidationError("слишком коротко")
    #     return user_name_surname
    #
    # def clean_text(self):
    #     text = self.cleaned_data['text']
    #     if len(text) < 3:
    #         raise ValidationError("слишком коротко")
    #
    #     return text

    # def clean_image(self):
    #     image = self.cleaned_data['image']
    #     if not image:
    #         raise ValidationError("вставте снимок")
    #     return image




class ReviewForm(forms.Form):
    default_doctor = Doctor.objects.first()
    doctor_choice = forms.ModelChoiceField(
        required=False,
        initial=default_doctor,
        queryset=Doctor.objects.filter(profile_id__is_superuser=False),
        label="Выберите Доктора",
        widget=forms.Select(
            attrs={
                'placeholder': 'Выберите доктора',
                'class': 'form-control',
                'id': 'doctor-review-choice'
            }
        )
    )
    text = forms.CharField(
        label="Отзыв",
        widget=forms.Textarea(
            attrs={
                'width': "100%", 'cols': "10", 'rows': "5",
                'placeholder': 'Напишите свой отзыв',
                'class': 'form-control',
                'id': 'review-text'
            }
        )
    )


class AppointmentForm(forms.Form):
    default_doctor = Doctor.objects.first()
    doctor_choice = forms.ModelChoiceField(
        required=False,
        initial=default_doctor,
        queryset=Doctor.objects.filter(profile_id__is_superuser=False),
        label="Выберите Доктора",
        widget=forms.Select(
            attrs={
                'placeholder': 'Выберите доктора',
                'class': 'form-control',
                'id': 'doctor-appointment-choice'
            }
        )
    )
    start_time = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        required=True,
        widget=forms.DateTimeInput(
            format='%d/%m/%Y %H:%M',
            attrs={
                'placeholder': 'Дата и Время *',
                'class': 'form-control date',
                'id': 'start-time-input'
            }
        )
    )
    text = forms.CharField(
        required=False,
        label="Предпочтение",
        widget=forms.Textarea(
            attrs={
                'width': "100%", 'cols': "10", 'rows': "5",
                'placeholder': 'Ваши предпочтения',
                'class': 'form-control',
                'id': 'appointment-text'
            }
        )
    )

