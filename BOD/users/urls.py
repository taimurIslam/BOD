from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include, re_path
from . import views
from .views import *
app_name = 'users'

urlpatterns = [
    re_path('login/', views.login, name='login'),
    re_path('logout/', views.logout, name='logout'),
    re_path('registration/', views.registration, name='registration'),
    re_path('user_list/', views.user_list, name='user_list'),
    re_path('user_edit/(?P<user_id>[0-9]+)/$', views.user_edit, name='user_edit'),
    re_path('user_delete/(?P<user_id>[0-9]+)/$', views.user_delete, name='user_delete'),

    re_path('roles/', views.roles_list, name='roles_list'),
    re_path('roles_add/', views.add_role, name='add_role'),
    re_path('roles_edit/(?P<role_id>[0-9]+)/$', views.edit_role, name='edit_role'),
    re_path('roles_delete/(?P<role_id>[0-9]+)/$', views.delete_role, name='delete_role'),

    url(r'^project_list/$', project_list, name='project_list'),
    url(r'^project_type_list/$', project_type_list, name='project_type_list'),
    url(r'^add_project/$', add_new_project, name='add_new_project'),
    url(r'^add_project_type/$', add_new_project_type, name='add_new_project_type'),
    url(r'^delete_project/(?P<pk>[0-9]+)/$', delete_project, name='delete_project'),
    url(r'^delete_project_type/(?P<pk>[0-9]+)/$', delete_project_type, name='delete_project_type'),
    url(r'^edit_project/(?P<pk>[0-9]+)/$', edit_project, name='edit_project'),
    url(r'^edit_project_type/(?P<pk>[0-9]+)/$', edit_project_type, name='edit_project_type'),

    # url(r'^roles/delete/(?P<role_id>[0-9]+)/$', delete_role, name='delete_role'),
]