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
from useraccount.models import User,MyInformation
from django.contrib.auth.mixins import UserPassesTestMixin



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
        if auth:
            user_save(request)
            messages.add_message(request,messages.INFO,"Success")
            return redirect("bank:home")
        return redirect("user:register")
        
    def get(self,request,*args,**kwargs):
        return render(request,"register.html")
    
class UserLogout(View,LoginRequiredMixin):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("bank:home")
    
    
    
    
class MyprofileView(LoginRequiredMixin,UserPassesTestMixin,View):
    def get(self,request,*args,**kwargs):
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
 

        
        
        
        
    
        




