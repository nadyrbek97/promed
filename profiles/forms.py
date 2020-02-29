from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField


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
        required=False,
        label="Ф.И.О пациента",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ф.И.О',
                'class': "form-control",
            }))
    email = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'name@example.com',
                'class': 'form-control'
            }
        )
    )
    text = forms.CharField(
        required=False,
        label="Текст заключения",
        widget=forms.Textarea(
            attrs={
                'width': "100%", 'cols': "100", 'rows': "20",
                'placeholder': 'Текст заключения',
                'class': 'form-control',
                'id': 'conclusion-text'
            }))
    image = forms.FileField(
        required=False,
        label="Выберите снимок",
        widget=forms.FileInput(
            attrs={
                'name': 'conclusion_image',
                'placeholder': 'Выберите снимок',
                'class': 'custom-file-input',
            }
        )
    )



