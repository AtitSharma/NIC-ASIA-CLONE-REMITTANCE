from django.contrib import admin
from useraccount.models import MyInformation,User


# Register your models here.


@admin.register(User)
class UserAsdmin(admin.ModelAdmin):
    list_display=["id","email","username","first_name","last_name"]
    
    
@admin.register(MyInformation)
class UserInformation(admin.ModelAdmin):
    list_display=["id","user","gender","account_number","photos","amount"]