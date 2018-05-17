from django.conf.urls import url
from .views import *
app_name='loginApp'

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^registration/$', RegView.as_view(), name='registration'),
    url(r'^role_wise_user_list/$', RoleWiseListView.as_view(), name='role_wise_user_list'),
    url(r'^update_user/$', UserUpdateView.as_view(), name='update_user'),
    url(r'^project_details/$', ProjectDetailsView.as_view(), name='project_details'),
    url(r'^project_list/$', ProjectListView.as_view(), name='project_list'),
    url(r'^project_assign/$', AddProjectView.as_view(), name='project_assign'),
    url(r'^project_type/$', ProjectTypeView.as_view(), name='project_type'),
    url(r'^user_list/$', UserListView.as_view(), name='user_list'),
    url(r'^user_project_list/$', UserProjectListView.as_view(), name='user_list'),

]