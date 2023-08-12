from useraccount.models import User,MyInformation,Token
from django.db.models import Q
from django.contrib import messages
import random

def authenticate_credentials(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password1=request.POST.get("password1")
    password2=request.POST.get("password2")
    if password1 ==password2:
        if len(password1)<5:
            messages.add_message(request,messages.INFO,"Length Of password must be 5")
            return False
        else:       
            user=User.objects.filter(Q(username=username) | Q(email=email))
            if not user:
                return True
            messages.add_message(request,messages.INFO,"User Having Such credentials Already Exits")
            return False
    messages.add_message(request,messages.INFO,"Both password Didnt matched")
    return False



def account_number_create():
    nums=[1,2,3,4,5,6,7,8,9,0]
    account_num=0
    for _ in range (16):
        num=random.choices(nums)
        account_num=account_num*10+num[0]
    return account_num




def user_save(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password1=request.POST.get("password1")
    user=User.objects.create_user(username=username,email=email,password=password1)
    user.is_active=False
    user.save()
    account_number=account_number_create()
    my_info=MyInformation.objects.filter(account_number=account_number).first()
    if my_info:
        account_number=account_number_create()   
    MyInformation.objects.create(user=user,account_number=account_number)
    return 

