from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from guardian.admin import GuardedModelAdmin
from . import models


# Register your models here.
class ProjectGuardianAdmin(GuardedModelAdmin):
    list_display = ['name', 'owner']
    fields = ['name', 'owner']


class HouseGuardianAdmin(GuardedModelAdmin):
    pass


@admin.register(models.User)
class UserAdmin(auth_admin.UserAdmin):
    # form = UserChangeForm
    # add_form = UserCreationForm
    model = models.User


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    fields = ['user']
    list_display = ['user']


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    fields = ['user']
    list_display = ['user']


admin.site.register(models.Project, ProjectGuardianAdmin)
admin.site.register(models.House, HouseGuardianAdmin)
