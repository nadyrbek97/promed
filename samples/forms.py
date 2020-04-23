from django import forms

from samples.models import Sample


class SampleForm(forms.ModelForm):
    title = forms.CharField(
        label="Название шаблона",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'sample-title-input'
            }
        )
    )
    description = forms.CharField(
        label="Описание",
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id': 'sample-description-input'
            }
        )
    )

    class Meta:
        model = Sample
        fields = ["title", "description"]


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