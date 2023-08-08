from django import forms
from useraccount.models import MyInformation



class UserLoginForm(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(min_length=5,max_length=100,widget=forms.PasswordInput)
    
    
    
class MyAccountUpdateForm(forms.Form):
    class Meta:
        model=MyInformation
        fields=["gender","photos",]
    
    