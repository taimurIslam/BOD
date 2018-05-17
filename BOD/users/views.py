from django.shortcuts import render, HttpResponse, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import ValidationError
import random
import hashlib
from django.core.mail import send_mail
from django.utils import timezone
#from .templates

# Create your views here.


def login(request):

    if 'logged_in' in request.session:
        if request.session['logged_in'] is True:
            return redirect('users:user_list')

    else:
        if request.method == 'GET':
            form = Login_Form()
            return render(request, 'users/login.html', {'form': form, 'browser_title': 'User Login'})


        elif request.method == 'POST':
            form_values = Login_Form(request.POST or None)
            if form_values.is_valid:
                user_username_or_email = form_values['user_username_or_email'].value()
                user_password = form_values['user_password'].value()

                try:
                    user = User.objects.get(Q(email=user_username_or_email)| Q(username= user_username_or_email), password = user_password)
                    if user.password == user_password:
                        if user.is_active is True:
                            request.session['logged_in'] = True
                            request.session['username'] = user.username
                            request.session['id'] = user.pk
                            request.session['photo'] = str(user.photo)
                            role = Role.objects.get(id = user.role_id)
                            request.session['role_title'] = role.role_title
                            return redirect('users:user_list')
                        else:
                            messages.error(request, 'Your Account is not active. Please contact Admin.' )
                    else:
                        messages.error(request, 'Incorrect Email or Password!')

                except User.DoesNotExist:
                    messages.error(request, 'No user found by the Email or Username Provided')

                return redirect('users:login')
# LOGOUT
def logout(request):
    if 'logged_in' in request.session:
        del request.session['logged_in']
        del request.session['username']
        del request.session['id']
        del request.session['role_title']
        del request.session['photo']
        return redirect('users:login')
    else:
        return redirect('users:login')


#Registration Form
def registration(request):
    arg = {}
    arg['form'] = Registration_Form
    arg['browser_title'] = 'Add New User'
    arg['heading_title'] = 'User Registration Form'
    arg['purpose'] = 'registration'
    arg['button'] = "Submit"
    if request.method == 'POST':
        form_values = Registration_Form(request.POST, request.FILES)
        if form_values.is_valid():
            data = form_values.save(commit=False)
            password = data.password.encode('utf-8')
            password = hashlib.sha256(password).hexdigest()
            data.password = password

            activation_code = str(random.randrange(0, 999999))
            data.activation_code = activation_code

            data.save()
            send_mail('registration Completed', 'Hello Taimur Your Registration is completed', 'smtp.gmail.com', ['taimur.joy@gmail.com'], fail_silently=False)
            return redirect('Users:registration')

        else:
            #messages.error(request, 'Incorrect Email or Password!')
            arg['form'] = form_values
            return render(request, 'users/form.html', arg)
    return render(request, 'users/form.html', arg)




#@login_required('logged_in', 'Users:login')
def user_list(request):
    arg = {}
    arg['users'] = User.objects.all()
    print(arg)
    if 'logged_in' in request.session:
        if request.session['logged_in'] is True:
            return render(request, 'users/user_list.html', arg)

    else:
        return redirect('users:login')
    return HttpResponse("hhh")

def user_edit(request, user_id):
    arg = {}
    try:
        user = User.objects.get(pk = user_id)
    except User.DoesNotExist:
        return HttpResponse('User Does Nor Exist')
    arg['form'] = Registration_Form(instance=user)
    arg['browser_title'] = 'Update User Data'
    arg['heading_title'] = 'Update User Data'
    arg['button'] = "Update"
    arg['purpose'] = 'update'
    arg['id'] = user_id

    if request.method == 'POST':
        update_form = Registration_Form(instance=user, data=request.POST, files=request.FILES)
        if update_form.is_valid():
            update_form.save()
            return redirect('users:user_list')
        else:
            arg['form'] = update_form
            return render(request, 'users/form.html', arg)

    return render(request, 'users/form.html', arg)

#-----------------------Delete A User----------------
def user_delete(request, user_id):
    if int(user_id) == request.session['id']:
        messages.error(request,'User Can not Delete Self')
    else:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return HttpResponse('User Does Nor Exist')
        user.delete()
        messages.success(request, 'User Deleted')

    return redirect('users:user_list')


def roles_list(request):
    roles = Role.objects.all()
    arg = {}
    arg['user'] = "active"
    arg['list_roles'] = "active"
    arg['title'] = "Roles List"
    arg['roles'] = roles
    arg['redirect_title'] = "Role List"
    arg['rediurect_url'] = "users:list_roles"
    return render(request, 'users/role_list.html', arg)

def add_role(request):
    arg = {}
    arg['user'] = "active"
    arg['list_roles'] = "active"
    arg['btn'] = "Save"
    arg['title'] = "Role Add"
    arg['redirect_title'] = "User List"
    arg['rediurect_url'] = "users:list_roles"
    arg['heading_title'] = 'Add New Role'
    arg['browser_title'] = 'Add New Role'
    arg['button'] = "Submit"

    if request.method == 'POST':

        form = RoleForm(request.POST, request.FILES)

        if form.is_valid():
            role = form.save()
            messages.success(request, 'Role Added')

            return redirect('users:roles_list')
    else:

        form = RoleForm()

    arg['form'] = form
    return render(request, 'users/form.html', arg)

def edit_role(request, role_id):
    try:
        role = Role.objects.get(id=role_id)
    except Role.DoesNotExist:
        return render(request, '404.html')

    arg = {}
    arg['user'] = "active"
    arg['list_roles'] = "active"
    arg['btn'] = "Save"
    arg['title'] = "Edit Role"
    arg['redirect_title'] = "Role List"
    arg['rediurect_url'] = "users:list_roles"
    arg['heading_title'] = 'Edit Role'
    arg['browser_title'] = 'Edit Role'
    arg['button'] = "Submit"
    arg['form'] = RoleForm(instance=role)

    if request.method == 'POST':

        form = RoleForm(request.POST, request.FILES, instance=role)

        if form.is_valid():
            role = form.save()
            messages.success(request, 'Role Updated')

            return redirect('users:roles_list')
        else:
            arg['form'] = form
            return render(request, 'users/form.html', arg)

    return render(request, 'users/form.html', arg)


def delete_role(request, role_id):
    try:
        role = Role.objects.get(id=role_id)
    except Role.DoesNotExist:
        return render(request, '404.html')
    role.delete()
    messages.success(request, 'Role Deleted')
    return redirect('users:roles_list')

def project_list(request):

    arg = {}
    arg['dashboard'] = ""
    arg['project'] = "active "
    arg['title'] = "Project List"
    arg['profile_name'] = request.session['username']
    arg['user_role'] = request.session['role_title']
    arg['browser_title'] = 'Project List'
    arg['heading_title'] = 'Project List'
    arg['projects'] = ProjectInfo.objects.all()
    return render(request, 'projects/project_list.html', arg )


def project_type_list(request):
    arg = {}
    arg['dashboard'] = ""
    arg['project'] = "active "
    arg['title'] = "Project Type List"
    arg['profile_name'] = request.session['username']
    arg['user_role'] = request.session['role_title']
    arg['browser_title'] = 'Project Type List'
    arg['heading_title'] = 'Project Type List'
    arg['projects_type'] = ProjectType.objects.all()
    return render(request, 'projects/project_type_list.html', arg)

def add_new_project(request):
    arg = {}
    arg['form'] = AddProjectForm
    arg['dashboard'] = ""
    arg['project'] = "active "
    arg['title'] = "Add Project"
    arg['profile_name'] = request.session['username']
    arg['user_role'] = request.session['role_title']
    arg['browser_title'] = 'Add New Project'
    arg['heading_title'] = 'Add New Project'
    arg['button'] = "ADD PROJECT"
    user = User.objects.get(pk=request.session['id'])
    if request.method == 'POST':
        form = AddProjectForm(request.POST)
        if form.is_valid():
            print("post post")
            add_project = form.save()
            add_project.created_by = user
            add_project.modified_by = user
            add_project.created_at = timezone.now()
            add_project.modified_at = timezone.now()
            add_project.save()
            messages.success(request, 'Project Created!!')
            return redirect('users:project_list')
        else:
            arg['form'] = form
            return render(request, 'users/form.html', arg)

    return render(request, 'users/form.html', arg)

def add_new_project_type(request):
    arg = {}
    arg['form'] = ProjectTypeForm
    arg['browser_title'] = 'Add New Project Type'
    arg['heading_title'] = 'Add New Project Type'
    arg['button'] = "ADD PROJECT TYPE"
    user = User.objects.get(pk=request.session['id'])

    if request.method == 'POST':
        form_values = ProjectTypeForm(request.POST)
        if form_values.is_valid():

            add_project_type = form_values.save()
            add_project_type.created_by = user
            add_project_type.modified_by = user
            add_project_type.created_at = timezone.now()
            add_project_type.modified_at = timezone.now()
            add_project_type.save()
            messages.success(request, 'Project Type Created!!')
            return redirect('users:project_type_list')

        else:
            arg['form'] = form_values
            return render(request, 'users/form.html', arg)
    return render(request, 'users/form.html', arg)


def delete_project(request, pk):

    try:
        project = ProjectInfo.objects.get(pk=pk)
    except ProjectInfo.DoesNotExist:
        messages.error(request, 'Project does not exist anymore')

    project.delete()
    messages.success(request, 'Project deleted')
    return redirect('users:project_list')

def delete_project_type(request, pk):

    try:
        projectType = ProjectType.objects.get(pk=pk)
    except ProjectType.DoesNotExist:
        messages.error(request, 'Project Type does not exist anymore')

    projectType.delete()
    messages.success(request, 'Project Type deleted')
    return redirect('users:project_type_list')

def edit_project(request, pk):
    try:
        project = ProjectInfo.objects.get(pk=pk)
    except ProjectInfo.DoesNotExist:
        messages.error(request, 'Project does not exist anymore')


    arg = {}
    arg['dashboard'] = ""
    arg['project'] = "active "
    arg['title'] = "Update Project Info"
    arg['box_title'] = "UPDATE PROJECT INFO"
    arg['profile_name'] = request.session['username']
    arg['form'] = UpdateProjectForm(instance=project)
    arg['browser_title'] = 'Update Project'
    arg['heading_title'] = 'Update Project'
    arg['button'] = "UPDATE PROJECT"
    arg['pk'] = pk
    arg['redirect_title'] = "Project List"
    arg['redirect_url'] = 'users:project_list'
    arg['submit_name'] = 'UPDATE INFO'
    user = User.objects.get(pk=request.session['id'])

    if request.method == 'POST':

        upd_form = UpdateProjectForm(instance=project, data=request.POST)

        if upd_form.is_valid():

            update_project = upd_form.save()
            update_project.modified_by = user
            update_project.modified_at = timezone.now()
            update_project.save()


            messages.success(request, 'Information Updated')
            return redirect('users:project_list')
        else:
            arg['form'] = upd_form
            return render(request, 'users/form.html', arg)
    return render(request, 'users/form.html', arg)

def edit_project_type(request, pk):
    try:
        projectType = ProjectType.objects.get(pk=pk)
    except ProjectType.DoesNotExist:
        messages.error(request, 'Project type does not exist anymore')


    arg = {}
    arg['dashboard'] = ""
    arg['project'] = "active "
    arg['title'] = "Update Project Type"
    arg['box_title'] = "UPDATE PROJECT TYPE"
    arg['profile_name'] = request.session['username']
    arg['form'] = UpdateProjectTypeForm(instance=projectType)
    arg['pk'] = pk
    arg['redirect_title'] = "Project Type List"
    arg['redirect_url'] = 'users:project_type_list'
    arg['browser_title'] = 'Update Project Type'
    arg['heading_title'] = 'Update Project Type'
    arg['button'] = "UPDATE TYPE"

    user = User.objects.get(pk=request.session['id'])

    if request.method == 'POST':

        upd_form = UpdateProjectTypeForm(instance=projectType, data=request.POST)

        if upd_form.is_valid():

            update_project = upd_form.save()
            update_project.modified_by = user
            update_project.modified_at = timezone.now()
            update_project.save()


            messages.success(request, 'Information Updated')
            return redirect('users:project_type_list')
        else:
            arg['form'] = upd_form
            return render(request, 'users/form.html', arg)
    return render(request, 'users/form.html', arg)
