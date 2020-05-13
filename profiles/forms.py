from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField


from profiles.models import User, UserPhoneNumber


class PatientCreateForm(forms.Form):
    full_name = forms.CharField(
        required=True,
        label="Ф.И.О ***",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'patient-full-name-input'
            }
        )
    )
    phone_number = forms.CharField(
        required=False,
        label="Номер телефона",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'patient-phone-number-input'
            }
        )
    )
    birth_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        required=True,
        label="Дата рождения ***",
        widget=forms.DateInput(
            format='%d/%m/%Y',
            attrs={
                'placeholder': 'выберите дату рождения',
                'class': 'form-control date',
                'id': 'birth-date-input'
            }
        )
    )
    address = forms.CharField(
        required=False,
        label="Адресс",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'patient-address-input'
            }
        )
    )
    email = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'name@example.com',
                'id': 'patient-email-input',
                'class': 'form-control'}
        )
    )


class PatientProfileUpdateForm(forms.Form):
    full_name = forms.CharField(
        label="Ф.И.О",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'profile-full-name-input'
            }
        )
    )
    address = forms.CharField(
        required=False,
        label="Адресс",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'profile-address-input'
            }
        )
    )

    email = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'name@example.com',
                'id': 'profile-email-input',
                'class': 'form-control'}))


class UserAddPhoneNumberForm(forms.ModelForm):
    number = forms.CharField(
        label="Номер телофона",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'add-doctor-number-input'
            }
        )
    )

    class Meta:
        model = UserPhoneNumber
        fields = ['number']


class DoctorProfileUpdateForm(forms.Form):
    full_name = forms.CharField(
        label="Ф.И.О",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'profile-full-name-input'
            }
        )
    )
    image = forms.FileField(
        required=False,
        label="Выберите снимок",
        widget=forms.FileInput(
            attrs={
                'name': 'conclusion_image',
                'class': 'custom-file-input',
                'placeholder': 'Выберите снимок',
                'id': 'doctor-image-input',
            }))


class UserLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={'autofocus': True,
               'class': 'form-control form-control-lg', 'placeholder': 'Логин'}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password',
                   'class': 'form-control form-control-lg',
                   'placeholder': 'Пароль'}),
    )

