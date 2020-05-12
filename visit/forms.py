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
