from django import forms
from .models import Role, User
from .models import *
from django.db import models
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

class Registration_Form(forms.ModelForm):
    CHOICES = [('1', 'Active',), ('0', 'Inactive',)]
    role = forms.ModelChoiceField(label= 'User Title', empty_label='Select User Role', queryset=Role.objects.all(), widget=forms.Select(attrs={'class': 'span8'}), required=True)
    is_active = forms.ChoiceField(label='Is Active', choices=CHOICES, required=True, widget=forms.RadioSelect)
    class Meta:
        model = User
        exclude = ('activation_code', 'password_reset_code')
        widgets = {
                'first_name'    : forms.TextInput(attrs={'type': 'text','placeholder':"First Name", 'title':'First Name', "class":'span8'}),
                'last_name'     : forms.TextInput(attrs={'type': 'text','placeholder': "Last Name",'title': 'Last Name', "class":'span8'}),
                'phone'         : forms.TextInput(attrs={'type': 'text','placeholder': "Phone Number",'pattern': '^[\+][8][8]\d{11}','title': 'Start with +88', "class":'span8'}),
                'email'         : forms.TextInput(attrs={'type': 'text', 'placeholder': "Enter Your Email ",'title': 'Enter Your Mail Here',"class": 'span8'}),
                'username'      : forms.TextInput(attrs={'type': 'text', 'placeholder': "User Name",'title': 'User Name', "class":'span8'}),
                'password'      : forms.TextInput(attrs={'type': 'password', 'placeholder': "User Password",'pattern': '[A-Za-z0-9]{3,11}', 'title': 'Minimum 3 character!',"class":'span8'}),
                'address'       : forms.TextInput(attrs={'type': 'text', 'placeholder': "User Address","class": 'span8'})
                 #'photo'        : forms.ImageField(label='Upload Photo')
                }
class Login_Form(forms.Form):
    user_username_or_email = forms.CharField(
        widget= forms.TextInput(
            attrs={
                'id' : "inputEmail",
                'class' : "span12",
                'placeholder': "User Name or Email",
                'autocomplete': 'off'
            }
        ))
    user_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'id' : "inputPassword",
                'class': "span12",
                'placeholder': "Password",
                'autocomplete': 'off'
            }
        ))
class PasswordResetForm(forms.Form):
    user_email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': "Enter Your Email",
            }
        ))

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = '__all__'
        widgets = {
            'role_title': forms.TextInput(attrs={'class': 'span8', 'placeholder': 'Role Title'})
        }

class ProjectTypeForm(forms.ModelForm):
    class Meta:
        model = Project_Type
        fields = ('name', 'code', 'details')
        widgets = {
            'name': forms.TextInput(attrs={"class": 'span8', 'required' : 'required','placeholder': 'Name'}),
            'code': forms.TextInput(attrs={"class": 'span8', 'required': 'required', 'placeholder': 'Code'}),
            'details': forms.TextInput(attrs={"class": 'span8', 'required': 'required', 'placeholder': 'Details'}),
        }

class UpdateProjectTypeForm(forms.ModelForm):
    class Meta:
        model = Project_Type
        fields = ('name', 'code', 'details')

        widgets = {

            'name': forms.TextInput(attrs={"class": 'span8', 'required' : 'required','placeholder': 'Name'}),
            'code': forms.TextInput(attrs={"class": 'span8', 'required': 'required', 'placeholder': 'Code'}),
            'details': forms.TextInput(attrs={"class": 'span8', 'required': 'required', 'placeholder': 'Details'}),
        }

class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project_Info
        fields = ('title', 'code', 'team_size', 'duration', 'response_day', 'budget', 'revenue_plan', 'target_revenue', 'additional_cost', 'type','details')

        widgets = {

            'title': forms.TextInput( attrs={"class": 'span8', 'required' : 'required','placeholder': 'Title'}),
            'code': forms.TextInput(attrs={"class": 'span8', 'required' : 'required','placeholder': 'Code'}),
            'team_size': forms.NumberInput(attrs={"class": 'span8', 'required': 'required', 'placeholder': 'Team Size'}),
            'duration': forms.NumberInput(attrs={"class": 'span8', 'required' : 'required','placeholder': 'Duration'}),
            'response_day': forms.NumberInput(attrs={"class": 'span8', 'required' : 'required', 'placeholder': 'Response Day'}),
            'budget': forms.TextInput(attrs={"class": 'span8', 'required' : 'required', 'placeholder': 'Budget'}),
            'revenue_plan': forms.TextInput(attrs={"class": 'span8', 'required': 'required', 'placeholder': 'Revenue Plan'}),
            'target_revenue': forms.TextInput(attrs={"class": 'span8', 'required': 'required', 'placeholder': 'Target Revenue'}),
            'additional_cost': forms.TextInput(attrs={"class": 'span8', 'required': 'required', 'placeholder': 'Additional Cost'}),
            'type': forms.Select(attrs={"class": 'span8', 'required': 'required', 'placeholder': 'Type'}),
            'details': forms.TextInput(attrs={"class": 'span8', 'required': 'required', 'placeholder': 'Details'}),
        }

class UpdateProjectForm(forms.ModelForm):
    class Meta:
        model = Project_Info
        fields = ('title', 'code', 'team_size', 'duration', 'response_day', 'budget', 'revenue_plan', 'target_revenue', 'additional_cost', 'type','details')

        widgets = {

            'title': forms.TextInput(attrs={"class": 'span8', 'required' : 'required','placeholder': 'Title'}),
            'code': forms.TextInput(attrs={"class": 'span8', 'required' : 'required','placeholder': 'Code'}),
            'team_size': forms.NumberInput(attrs={"class": 'span8', 'required': 'required', 'placeholder': 'Team Size'}),
            'duration': forms.NumberInput(attrs={"class": 'span8', 'required' : 'required','placeholder': 'Duration'}),
            'response_day': forms.NumberInput(attrs={"class": 'span8', 'required' : 'required', 'placeholder': 'Response Day'}),
            'budget': forms.TextInput(attrs={"class": 'span8', 'required' : 'required', 'placeholder': 'Budget'}),
            'revenue_plan': forms.TextInput(attrs={"class": 'span8', 'required': 'required', 'placeholder': 'Revenue Plan'}),
            'target_revenue': forms.TextInput(attrs={"class": 'span8', 'required': 'required', 'placeholder': 'Target Revenue'}),
            'additional_cost': forms.TextInput(attrs={"class": 'span8', 'required': 'required', 'placeholder': 'Additional Cost'}),
            'type': forms.Select(attrs={"class": 'span8', 'required': 'required', 'placeholder': 'Type'}),
            'details': forms.TextInput(attrs={"class": 'span8', 'required': 'required', 'placeholder': 'Details'}),
        }