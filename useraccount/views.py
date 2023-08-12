from typing import Optional
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.views import View
from useraccount.forms import UserLoginForm
from useraccount.authenticate import authenticate_credentials,user_save
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from useraccount.models import MyInformation
import json
from django.http import JsonResponse
from useraccount.models import User,MyInformation,Token
# from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from useraccount.mails import send_mail_to_user

class LoginUser(View):
    def post(self,request,*args,**kwargs):
        form=UserLoginForm(request.POST)
        if form.is_valid():
            email=request.POST.get("email")
            password=request.POST.get("password")
            user=authenticate(email=email,password=password)
            if user:
                login(request,user)
                messages.add_message(request,messages.INFO,"Login Successfully !!")
                messages.add_message(request,messages.INFO,"Make Sure To edit You information from My Profile !!")
                return redirect("bank:home")
        messages.add_message(request,messages.INFO,"Login Failed")
        return redirect("user:login")
    
    def get(self,request,*args,**kwargs):
        return render(request,"login.html")



class RegisterUser(View):
    def post(self,request,*args,**kwargs):
        auth=authenticate_credentials(request)
        email=request.POST.get("email")
        if auth:
            user_save(request)
            messages.add_message(request,messages.INFO,
            f"Dear User a E-Mail has been Sent To Your mail {email} Make\
            Sure To verify from the email ")
            send_mail_to_user(email)
            return redirect("bank:home")
        return redirect("user:register")
        
    def get(self,request,*args,**kwargs):
        return render(request,"register.html")
    
class UserLogout(View,LoginRequiredMixin):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("bank:home")
    
class MyprofileView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        test=self.test_func()
        if not test:
            raise PermissionDenied()
        pk=self.kwargs.get("pk")
        my_information=MyInformation.objects.filter(user__id=pk).first()
        context={
            "my_info":my_information
        }
        return render(request,"my_profile.html",context)
    
    
    def post(self,request,*args,**kwargs):
        data=json.loads(request.body)
        pk=self.kwargs.get("pk")
        first_name=data.get("firstname")
        last_name=data.get("lastname")
        gender=data.get("gender")

        if first_name=='' or last_name=='':
            return JsonResponse({"message":"Field is required !!!"})
        else:
            User.objects.filter(id=request.user.id).update(first_name=first_name,last_name=last_name)
            MyInformation.objects.filter(pk=pk).update(gender=gender)
            return JsonResponse({"message":"Succesfully Updated"})
        
        
    def test_func(self):
        pk=self.kwargs.get("pk")
        user=MyInformation.objects.filter(user__pk=pk).first()
        if not user:
            return False
        if user.user != self.request.user :
            return False
        return True
 
 
 
class VerifyTokenView(View):
    def get(self,request,*args,**kwargs):
        token=self.kwargs.get("token")
        user_token=Token.objects.filter(key=token).first()
        if user_token:
            user=user_token.user
            user.is_active=True
            user.save()
            messages.add_message(request,messages.INFO,"Successfully Verified Procceed To Login")
            return redirect("bank:home")
        messages.add_message(request,messages.INFO,"Verification Failed ")
        return redirect("bank:home")  
            
            

        
        
        
        
    
        




