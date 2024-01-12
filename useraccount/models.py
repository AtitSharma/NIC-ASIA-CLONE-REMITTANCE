from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractUser
from datetime import timedelta
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import uuid



class CustomUserManager(BaseUserManager):
    '''
        Custom Manager to Create User and SuperUser
    '''
    def create_user(self,email,password=None,**extra_fields):
        '''
            Create Normal Users
        '''
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
        '''
            Create Super User
        '''
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True ")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        '''
            Super must have all properties of normal user
        '''
        return self.create_user(email,password,**extra_fields)
        



class User(AbstractUser):
    email=models.EmailField(unique=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects=CustomUserManager()
    class Meta:
        verbose_name='User'
        verbose_name_plural="Users"
        
    def __str__(self):
        return self.username
        
  
  
class GenderChoices(models.TextChoices):
    MALE="male","MALE"
    FEMALE="female","FEMALE"
    OTHERS="others",'OTHERS'

      

class MyInformation(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    gender=models.CharField(max_length=100,choices=GenderChoices.choices,default=GenderChoices.MALE)
    account_number=models.IntegerField(unique=True)
    photos=models.ImageField(upload_to="posts/",blank=True,null=True)
    amount=models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username
    
    

    
    
class Token(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    key=models.CharField(max_length=40, primary_key=True,unique=True)
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.key)
    
    def is_valid(self):
        expiration_time = self.created + timedelta(minutes=1)
        return timezone.now() <= expiration_time
    
    def save(self,*args,**kwargs):
        self.key=str(uuid.uuid4())
        super().save(*args,**kwargs)
        
        
        
# class Otp(models.Model):
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#     key=models.CharField(max_length=40, primary_key=True,unique=True)
#     created=models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return str(self.key)
    
#     def is_valid(self):
#         expiration_time = self.created + timedelta(minutes=1)
#         return timezone.now() <= expiration_time
    
    
    
    
