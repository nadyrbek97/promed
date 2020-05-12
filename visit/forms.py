from django import forms

from profiles.models import Doctor


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

