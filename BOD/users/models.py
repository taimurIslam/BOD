from django.db import models
from imagekit.conf import ImageKitConf
from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize

# Create your models here.

#------------------------------------------------#
# User Role models
class Role(models.Model):
    role_title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.role_title
    def as_json(self):
        return dict(
            role_title = str(self.role_title),
        )
#------------------------------------------------#
#------------------------------------------------#
# User models
class User(models.Model):

    ImageKitConf.CACHEFILE_DIR = 'uploads/200/'

    first_name = models.CharField(max_length=30)
    last_name  = models.CharField(max_length=20)
    username   = models.CharField(max_length=30, unique=True)
    password   = models.CharField(max_length=100)
    email      = models.EmailField(unique=True)
    phone      = models.CharField(max_length=20)
    address    = models.CharField(max_length=100)
    user_type  = models.CharField(max_length=20)
    designation = models.CharField(max_length=100)

    photo      = models.ImageField(upload_to='uploads/200/', default='uploads/200/default.png', blank=True)
    thumb      = ImageSpecField(source = 'photo', processors=[SmartResize(200,200)],)

    role       = models.ForeignKey('Role', default=1, on_delete=models.CASCADE)
    is_active  = models.BooleanField(default=True)

    activation_code = models.CharField(max_length=50)
    password_reset_code = models.CharField(max_length=50, default=0)

    def as_json(self):
        return dict(
            first_name=str(self.first_name),
            last_name=str(self.last_name),
            username=str(self.username),
            email=str(self.email),
            phone=str(self.phone),
            address=str(self.address),
            designation = str(self.designation),
            user_type = str(self.user_type),
            photo=str(self.photo),
            role_id=self.role_id,
            is_active=(self.is_active),
        )

    def as_json_with_password(self):
        return dict(
            id=int(self.pk),
            password=str(self.password)
        )
    def is_authenticated(self):
        pass
#------------------------------------------------------#

class Project_Type(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, unique=True)
    details = models.CharField(max_length=50)
    created_at = models.DateTimeField(editable=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey('users.User', null=True, blank=True, on_delete=models.CASCADE, related_name='created_by+')
    modified_by = models.ForeignKey('users.User', null=True, blank=True, on_delete=models.CASCADE, related_name='modified_by+')
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Project_Info(models.Model):
    title = models.CharField(max_length=50)
    code = models.CharField(max_length=20, unique=True)
    team_size = models.IntegerField()
    duration = models.IntegerField()
    response_day = models.IntegerField()
    budget = models.FloatField()
    revenue_plan = models.FloatField()
    target_revenue = models.FloatField()
    additional_cost = models.FloatField()
    type = models.ForeignKey('Project_Type', default=1, on_delete=models.CASCADE)
    details = models.TextField()
    created_at = models.DateTimeField(editable=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey('users.User', null=True, blank=True, on_delete=models.CASCADE,
                                   related_name='created_by+')
    modified_by = models.ForeignKey('users.User', null=True, blank=True, on_delete=models.CASCADE,
                                    related_name='modified_by+')
    status = models.IntegerField(default=0)

    def as_json(self):

        return dict(

            type_id=self.type_id,

        )


class Project_Manager(models.Model):
    project = models.ForeignKey('users.Project_Info', default=1, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey('users.User', default=1, on_delete=models.CASCADE, related_name='assigned_by+')
    assigned_to = models.ForeignKey('users.User', default=1, on_delete=models.CASCADE, related_name='assigned_to+')
    created_at = models.DateTimeField(editable=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey('users.User', null=True, blank=True, on_delete=models.CASCADE,
                                   related_name='created_by+')
    modified_by = models.ForeignKey('users.User', null=True, blank=True, on_delete=models.CASCADE,
                                    related_name='modified_by+')
    status = models.IntegerField(default=0)




