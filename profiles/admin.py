from .models import (User,
                     Doctor,
                     Patient,
                     UserPhoneNumber)
from profiles.choices import ROLE

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'role', 'password1', "password2"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['username', 'role', 'gender', 'full_name',
                  'birth_date', 'email', 'password', ]

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserPhoneNumberInline(admin.StackedInline):
    model = UserPhoneNumber
    extra = 1


class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    inlines = [UserPhoneNumberInline]
    list_display = ('role', 'full_name')
    list_filter = ('role',)
    # fieldsets while creating user
    fieldsets = (
        (None, {'fields': ('username', 'role', 'email', 'password',)}),
        ('Personal info', {'fields': ('birth_date', 'gender', 'full_name')}),
    )
    # # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # # overrides get_fieldsets to use this attribute when creating a user.
    # fieldsets while adding user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'role', 'password1', 'password2')}
        ),
    )
    search_fields = ('full_name', 'username')
    ordering = ('-created',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, MyUserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
admin.site.register(Doctor)


class PatientAdmin(admin.ModelAdmin):
    ordering = ('-profile_id__created', )
    list_display = ('full_name', 'username')
    search_fields = ('profile_id__full_name', )
    list_per_page = 10

    def full_name(self, obj):
        return obj.profile_id.full_name

    def username(self, obj):
        return obj.profile_id.username


admin.site.register(Patient, PatientAdmin)

