from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ProjectsListView.as_view(), name='project-list' ),
    path('list/', views.list, name='project-list-1' ),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]