from django import forms
from django.forms import ValidationError
from django.contrib.auth.forms import AuthenticationForm, UsernameField

from profiles.models import User, UserPhoneNumber


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


class ConclusionForm(forms.Form):
    user_name_surname = forms.CharField(
        label="Ф.И.О пациента",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ф.И.О',
                'class': "form-control", }))
    email = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'name@example.com',
                'class': 'form-control'}))
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
            }))

    def clean_user_name_surname(self):
        user_name_surname = self.cleaned_data['user_name_surname']
        if len(user_name_surname) < 5:
            raise ValidationError("слишком коротко")
        return user_name_surname

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) < 10:
            raise ValidationError("слишком коротко")

        return text

    # def clean_image(self):
    #     image = self.cleaned_data['image']
    #     if not image:
    #         raise ValidationError("вставте снимок")
    #     return image

