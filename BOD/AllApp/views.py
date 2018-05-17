from django.shortcuts import render
from rest_framework.validators import ValidationError
from rest_framework.views import Response
from .serializers import *
import requests
from requests.exceptions import ConnectionError
from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView
from django.db.models import Q
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from django.utils import timezone

# Create your views here.

class LoginView(CreateAPIView):



    def post(self, request, *args, **kwargs):
        if 'email' not in request.POST or request.POST['email'] is '':
            raise ValidationError({'message': 'Email is needed', 'status_code': '400'})

        if 'password' not in request.POST or request.POST['password'] is '':
            raise ValidationError({'message': 'Password is needed', 'status_code': '400'})

        email = request.POST['email']
        user_password = request.POST['password']

        try:
            renter = User.objects.get(email=email)

            if renter.is_active != "1":
                return Response({'message': 'User is not active', 'status_code': '400', 'activation code': renter.is_active})
            else:
                if renter.password == user_password:
                    return Response({'message': 'success', 'status_code': '200'})
                else:
                    return Response({'message': 'failed', 'status_code': '400'})



        except User.DoesNotExist:
            return Response({'message': 'User does not exist', 'status_code': '400'})


class RegView(CreateAPIView):
    renderer_classes = (JSONRenderer,)


    def post(self, request, format=None):
        if 'first_name' not in request.POST or request.POST['first_name'] is '':
            raise ValidationError({'message': 'First Name is needed', 'status_code': '400'})

        if 'last_name' not in request.POST or request.POST['last_name'] is '':
            raise ValidationError({'message': 'Last Name is needed', 'status_code': '400'})

        if 'email' not in request.POST or request.POST['email'] is '':
            raise ValidationError({'message': 'Email is needed', 'status_code': '400'})

        if 'password' not in request.POST or request.POST['password'] is '':
            raise ValidationError({'message': 'Password is needed', 'status_code': '400'})


        if 'user_name' not in request.POST or request.POST['user_name'] is '':
            raise ValidationError({'message': 'User Name is needed', 'status_code': '400'})

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        user_password = request.POST['password']
        user_name = request.POST['user_name']

        try:
            renter = User.objects.get(Q(email=email) | Q(user_name=user_name))
            return Response({'message': 'User is already existed', 'status_code': '400'})

        except User.DoesNotExist:
            create_user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=user_password,
                user_name=user_name,

            )
            response = {
                'first_name': str(first_name),
                'last_name': str(last_name),
                'email': str(email),
                'password': str(user_password),
                'user_name': str(user_name)

            }


            return JsonResponse( {'message': 'suceess', 'status_code': '200', 'data': response})

class RoleWiseListView(CreateAPIView):
    serializer_class = UserSerializer
    renderer_classes = (JSONRenderer,)


    def post(self, request, format=None):
        if 'role_id' not in request.POST or request.POST['role_id'] is '':
            raise ValidationError({'message': 'Role ID is needed', 'status_code': '400'})

        role_id = request.POST['role_id']


        user_details = User.objects.filter(user_role=role_id)

        if not user_details:
            return Response({'message': 'User Does Not Exist', 'status_code': '400'})

        user_response = list()
        for user_details in user_details:
            user_response.append(
                {
                    'first_name': str(user_details.first_name),
                    'last_name': str(user_details.last_name),
                    'email': str(user_details.email),
                    'password': str(user_details.password),
                    'user_name': str(user_details.user_name),
                    'user_role': str(user_details.user_role),
                    'is_active': str(user_details.is_active)

                }

            )

        return JsonResponse({'message': 'suceess', 'status_code': '200', 'data': user_response})


class UserUpdateView(CreateAPIView):
    serializer_class = UserSerializer
    renderer_classes = (JSONRenderer,)


    def post(self, request, format=None):

        if 'user_id' not in request.POST or request.POST['user_id'] is '':
            raise ValidationError({'message': 'User ID is needed', 'status_code': '400'})

        if 'first_name' not in request.POST or request.POST['first_name'] is '':
            raise ValidationError({'message': 'First Name is needed', 'status_code': '400'})

        if 'last_name' not in request.POST or request.POST['last_name'] is '':
            raise ValidationError({'message': 'Last Name is needed', 'status_code': '400'})

        if 'email' not in request.POST or request.POST['email'] is '':
            raise ValidationError({'message': 'Email is needed', 'status_code': '400'})

        if 'password' not in request.POST or request.POST['password'] is '':
            raise ValidationError({'message': 'Password is needed', 'status_code': '400'})

        if 'is_active' not in request.POST or request.POST['is_active'] is '':
            raise ValidationError({'message': 'Activation ID is needed', 'status_code': '400'})

        if 'role_id' not in request.POST or request.POST['role_id'] is '':
            raise ValidationError({'message': 'Role ID is needed', 'status_code': '400'})

        if 'user_name' not in request.POST or request.POST['user_name'] is '':
            raise ValidationError({'message': 'User Name is needed', 'status_code': '400'})
        try:
            renter = User.objects.get(Q(email=request.POST['email']) | Q(user_name=request.POST['user_name']))
            if(renter.email==request.POST['email']):
                return Response({'message': 'Email already existed', 'status_code': '400'})
            if(renter.user_name==request.POST['user_name']):
                return Response({'message': 'User Name already existed', 'status_code': '400'})

        except:
            user_id = request.POST['user_id']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            user_password = request.POST['password']
            is_active = request.POST['is_active']
            # if is_active != 0 or is_active != 1:
            #     return Response({'message': 'Value must be 0 or 1 in Activation Code', 'status_code': '400', 'Activation Code': is_active })
            role_id = request.POST['role_id']
            # if (role_id != '1' or role_id != '2' or role_id!='3'):
            #     return Response({'message': 'Value must be 1 or 2 or 3 in Role ID', 'status_code': '400'})
            try:
                role_details = Role.objects.get(pk=role_id)
            except Role.DoesNotExist:
                return Response({'message': 'role Does Not Exist', 'status_code': '400'})

            user_name = request.POST['user_name']



            try:
                user_details = User.objects.get(pk=user_id)
                user_details.first_name=first_name
                user_details.last_name=last_name
                user_details.email=email
                user_details.password=user_password
                user_details.is_active=is_active
                user_details.user_role_id=role_id
                user_details.user_name=user_name
                user_details.save()

                response = {
                    'first_name': str(first_name),
                    'last_name': str(last_name),
                    'email': str(email),
                    'password': str(user_password),
                    'is_active': str(is_active),
                    'user_role' : str(role_id),
                    'user_name': str(user_name)

                }
                return JsonResponse({'message': 'suceess', 'status_code': '200', 'data': response})

            except User.DoesNotExist:
                return Response({'message': 'User Does Not Exist', 'status_code': '400'})


class ProjectDetailsView(CreateAPIView):
    serializer_class = ProjectSerializer
    renderer_classes = (JSONRenderer,)


    def post(self, request, format=None):

        if 'project_id' not in request.POST or request.POST['project_id'] is '':
            raise ValidationError({'message': 'Project ID is needed', 'status_code': '400'})

        project_id = request.POST['project_id']

        try:
            project_details = ProjectInfo.objects.get(pk=project_id)
        except ProjectInfo.DoesNotExist:
            return Response({'message': 'project Does Not Exist', 'status_code': '400'})


        return JsonResponse({'message': 'suceess', 'status_code': '200', 'title': str(project_details.title),
                'code': str(project_details.code),
                'team_size': str(project_details.team_size),
                'duration': str(project_details.duration),
                'response_day': str(project_details.response_day),
                'budget': str(project_details.budget),
                'revenue_plan': str(project_details.revenue_plan),
                'target_revenue': str(project_details.target_revenue),
                'additional_cost': str(project_details.additional_cost),
                'type': str(project_details.type),
                'details': str(project_details.details) })


class ProjectListView(CreateAPIView):
    serializer_class = ProjectSerializer
    renderer_classes = (JSONRenderer,)

    def post(self, request, format=None):




        project_lists = ProjectInfo.objects.all()

        project_response = list()
        for project_list in project_lists:
            project_response.append(
                {
                    'id': str(project_list.id),
                    'title': str(project_list.title),
                    'code': str(project_list.code),

                }

            )

        return JsonResponse({'message': 'suceess', 'status_code': '200', 'data': project_response})


class AddProjectView(CreateAPIView):
    serializer_class = ProjectManagerSerializer, ProjectManagerSerializer

    def post(self, request, format=None):

        if 'title' not in request.POST or request.POST['title'] is '':
            raise ValidationError({'message': 'Project Title is needed', 'status_code': '400'})
        if 'code' not in request.POST or request.POST['code'] is '':
            raise ValidationError({'message': 'Code is needed', 'status_code': '400'})
        if 'details' not in request.POST or request.POST['details'] is '':
            raise ValidationError({'message': 'Details is needed', 'status_code': '400'})
        if 'team_size' not in request.POST or request.POST['team_size'] is '':
            raise ValidationError({'message': 'Team Size is needed', 'status_code': '400'})
        if 'duration' not in request.POST or request.POST['duration'] is '':
            raise ValidationError({'message': 'Duration is needed', 'status_code': '400'})
        if 'response_day' not in request.POST or request.POST['response_day'] is '':
            raise ValidationError({'message': 'Response Day is needed', 'status_code': '400'})
        if 'budget' not in request.POST or request.POST['budget'] is '':
            raise ValidationError({'message': 'Budget is needed', 'status_code': '400'})
        if 'revenue_plan' not in request.POST or request.POST['revenue_plan'] is '':
            raise ValidationError({'message': 'Revenue Plan is needed', 'status_code': '400'})
        if 'duration' not in request.POST or request.POST['duration'] is '':
            raise ValidationError({'message': 'Duration is needed', 'status_code': '400'})
        if 'response_day' not in request.POST or request.POST['response_day'] is '':
            raise ValidationError({'message': 'Response Day is needed', 'status_code': '400'})
        if 'budget' not in request.POST or request.POST['budget'] is '':
            raise ValidationError({'message': 'Budget is needed', 'status_code': '400'})
        if 'revenue_plan' not in request.POST or request.POST['revenue_plan'] is '':
            raise ValidationError({'message': 'Revenue Plan is needed', 'status_code': '400'})



        project_id = request.POST['project_id']
        try:
            project = ProjectInfo.objects.get(pk=project_id)
        except ProjectInfo.DoesNotExist:
            return Response({'message': 'project Does Not Exist', 'status_code': '400'})

        assigned_by = request.POST['assigned_by']


        assigned_to=(request.POST['assigned_to'])
        new_assigned_to= assigned_to.split(",")

        created_by = request.POST['created_by']

        try:
            user = User.objects.get(first_name=created_by)
        except ProjectInfo.DoesNotExist:
            return Response({'message': 'User Does Not Exist', 'status_code': '400'})


        for person in new_assigned_to:
            assign_project = ProjectManager.objects.create(
                project_id = project,
                assigned_by = assigned_by,
                assigned_to = person,
                created_by = user,
                modified_by = user,
                created_at = timezone.now(),
                modified_at = timezone.now(),

            )
        return JsonResponse({'message': 'suceess', 'status_code': '200'})

class ProjectTypeView(CreateAPIView):
    serializer_class = ProjectTypeSerializer

    def post(self, request, format=None):

        try:
            all_project_type = ProjectType.objects.all()
        except ProjectType.DoesNotExist:
            return Response({'message': ' No Project Exist', 'status_code': '400'})

        project_type = list()
        for project_type_info in all_project_type:
            project_type.append(
                {
                'id': str(project_type_info.id),
                'project name': str(project_type_info.name),
                }
            )

        return JsonResponse({'project type': project_type, 'message': 'success', 'status_code': '200'})

class UserListView(CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, format=None):
        try:
            all_user = User.objects.all()
        except User.DoesNotExist:
            return Response({'message': 'No User Exist', 'status_code': '400'})

        user_list = list()
        for user in all_user:
            user_list.append(
                {
                    'id': user.id,
                    'first name' : user.first_name,
                    'last name' : user.last_name,
                    'username': user.username,
                    'email': user.email,
                    'phone number': user.phone,
                    'address': user.address,
                    'status':user.is_active,

                }

            )
        return JsonResponse({'user list': user_list,'message': 'success', 'status_code': '200'})


class UserProjectListView(CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, format=None):
        if 'user_id' not in request.POST or request.POST['user_id'] is '':
            raise ValidationError({'message': 'User ID is needed', 'status_code': '400'})

        user_id = request.POST['user_id']

        try:
            user_all_project = ProjectInfo.objects.filter(created_by_id=user_id)
        except User.DoesNotExist:
            return Response({'message': 'No Project Exist For The User', 'status_code': '400'})

        project_list = list()
        for project_info in user_all_project:
            project_list.append(
                {
                    'project id': project_info.id,
                    'project title' : project_info.title,
                    'project code' : project_info.code,
                    'team size': project_info.team_size,
                    'duration': project_info.duration,
                    'response day': project_info.response_day,
                    'budget': project_info.budget,
                    'revenue plan': project_info.revenue_plan,
                    'target revenue': project_info.target_revenue,
                    'additional cost': project_info.additional_cost,
                    'details': project_info.details,



                }

            )
        return JsonResponse({'user all project list': project_list,'message': 'success', 'status_code': '200'})