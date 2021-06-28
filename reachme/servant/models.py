from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.db.models.signals import post_delete
from django.dispatch import receiver
import django.utils.timezone
from django.contrib.auth.hashers import make_password,mask_hash

class MyUserManager(BaseUserManager):
    def create_user(self,email,password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user=self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password=None):
        user=self.create_user(
            email,
            password=password,
        )
        user.is_admin=True
        user.save(using=self._db)
        return user





user_role_choices =  ( (1, "MSEB Chief Engineer"), 
   (2, "Health Department"), 
   (3, "Water Conservation officer"), 
   (4, "Municipal corporation"), 
   (5, "Department Safety Officer"), 
) 

class Users(AbstractBaseUser):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    aadhar_no = models.CharField(max_length=15,unique=True,default=None,blank=True,null=True)
    user_role = models.SmallIntegerField(default=0,choices=user_role_choices) 
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    no_of_complaint =  models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    upload_aadhar = models.FileField(upload_to="media/servant_aadhar")
    upload_id = models.FileField(upload_to="media/servant_doc")

    objects = MyUserManager()
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    DEFAULT_USER_ATTRIBUTES = ('first_name', 'last_name', 'email')
  
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin       


@receiver(post_delete, sender=Users)
def Users_file_delete(sender, instance, **kwargs):
    instance.upload_aadhar.delete(False) 
    instance.upload_id.delete(False)   