from django import forms

from profiles.models import Doctor


class AppointmentForm(forms.Form):
    patient_full_name = forms.CharField(
        required=True,
        label="Ф.И.О пациента",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ф.И.О *',
                'class': "form-control", }
        )
    )
    patient_phone_number = forms.CharField(
        required=True,
        label="Номер телефона",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Номер телефона',
                'class': "form-control",
                'id': 'patient-phone-number'
            }
        )
    )
    doctor_choice = forms.ModelChoiceField(
        required=False,
        queryset=Doctor.objects.filter(profile_id__is_superuser=False),
        label="Выберите Доктора",
        widget=forms.Select(
            attrs={
                'placeholder': 'Выберите доктора',
                'class': 'form-control',
                'id': 'doctor-choice',
                'style': 'select option {'
                         'background: #cccccc'
                         '}'
            }
        )
    )
    date_time = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        required=True,
        widget=forms.DateTimeInput(
            format='%d/%m/%Y %H:%M',
            attrs={
                'placeholder': 'Дата и Время *',
                'class': 'form-control date',
                'id': 'probootstrap-date'
            }
        )
    )
    patient_preference = forms.CharField(
        required=False,
        label="Предпочтения пациента",
        widget=forms.Textarea(
            attrs={
                'width': "100%", 'cols': "100", 'rows': "5",
                'placeholder': 'Ваши предпочтения',
                'class': "form-control", }
        )
    )
