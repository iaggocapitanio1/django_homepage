from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from collections.abc import Iterable
from django.shortcuts import render, redirect
from django.db.models.signals import post_save
from django.views.generic import ListView
from typing import List
from django.contrib import messages
from django.dispatch import receiver
from django.core.exceptions import ImproperlyConfigured
from guardian.mixins import PermissionListMixin, PermissionRequiredMixin
from django.conf import settings
from . import models
from guardian.shortcuts import assign_perm, get_objects_for_user
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db.models.signals import pre_delete


# from guardian.models import User
# from guardian.models import UserObjectPermission
# from guardian.models import GroupObjectPermission
# def remove_obj_perms_connected_with_user(sender, instance, **kwargs):
# filters = Q(content_type=ContentType.objects.get_for_model(instance),
# object_pk=instance.pk)
# UserObjectPermission.objects.filter(filters).delete()
# GroupObjectPermission.objects.filter(filters).delete()
# pre_delete.connect(remove_obj_perms_connected_with_user, sender=User)
#
# # Create your views here.

class ProjectsListView(PermissionRequiredMixin, PermissionListMixin, ListView):
    template_name = 'home/projects.html'
    model = models.Project
    permission_required = ["homepage.view_project"]
    object_permission = ["read_project"]
    redirect_field_name = 'next'
    login_url = 'login/'

    get_objects_for_user_extra_kwargs = {}

    def get_object_permission(self, request: HttpRequest = None) -> List[str]:
        if isinstance(self.object_permission, str):
            perms = [self.object_permission]
        elif isinstance(self.object_permission, Iterable):
            perms = [p for p in self.object_permission]
        else:
            raise ImproperlyConfigured("'PermissionRequiredMixin' requires "
                                       "'permission_required' attribute to be set to "
                                       "'<app_label>.<permission codename>' but is set to '%s' instead"
                                       % self.permission_required)
        return perms

    def get_get_objects_for_user_kwargs(self, queryset):
        return dict(user=self.request.user,
                    perms=self.get_object_permission(self.request),
                    klass=queryset,
                    **self.get_objects_for_user_extra_kwargs)


def list(request: HttpRequest) -> HttpResponse:
    template_name = 'home/projects.html'
    context = dict(object_list=get_objects_for_user(user=request.user, klass=models.Project,
                                                    perms="read_project"))
    return render(request, template_name, context)


def login_user(request: HttpRequest) -> HttpResponse:
    template_name = 'authenticate/login.html'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('project-list')
        else:
            messages.info(request, "Usuário ou senha estão incorretos!", extra_tags='alert alert-danger message')
    context = dict()
    return render(request, template_name=template_name, context=context)


def logout_user(request):
    logout(request)
    return redirect('project-list')


@receiver(post_save, sender=models.Project)
def user_post_save(sender, **kwargs):
    """
    Create a Profile instance for all newly created User instances. We only
    run on user creation to avoid having to check for existence on each call
    to User.save.
    """
    project: models.Project = kwargs["instance"]
    created: bool = kwargs["created"]
    if created:
        user = models.User.objects.get(pk=project.owner.user.id)
        assign_perm("read_project", user, project)
