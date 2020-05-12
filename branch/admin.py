from django.contrib import admin

from .models import (Branch,
                     BranchPhoneNumber)


class BranchPhoneNumberInline(admin.StackedInline):
    model = BranchPhoneNumber
    extra = 1


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("title", "address", )
    inlines = [BranchPhoneNumberInline, ]
