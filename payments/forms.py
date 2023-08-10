from typing import Any, Dict
from django import forms
from useraccount.models import User,MyInformation



class CashTransferForm(forms.Form):     

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CashTransferForm, self).__init__(*args, **kwargs)

    cardnumber=forms.CharField(max_length=16,min_length=16)
    amount=forms.CharField()
    
    
    
    def clean_cardnumber(self):
        card_number=self.cleaned_data.get("cardnumber")
        try:
            card_number=int(card_number)
        except:
            raise forms.ValidationError("No Such User With Such Card Number !!")
        my_info=MyInformation.objects.filter(account_number=card_number)
        if not my_info:
            raise forms.ValidationError("No Such User With Such Card Number !!")
        return card_number
    
    
    def clean_amount(self):
        amount=self.cleaned_data.get("amount")
        try:
            amount=int(amount)
        except:
            raise forms.ValidationError(" Invalid Number for Amount !!")
        card_number=self.cleaned_data.get("cardnumber")
        if not card_number:
            raise forms.ValidationError("Error")
        my_card_number=self.request.POST.get('cardnumber-my')
        my_info=MyInformation.objects.filter(account_number=my_card_number).first()
        if my_info.amount < int(amount):
            raise forms.ValidationError("Insufficient Funds")
        return amount
        
    def clean(self):
        user=self.request.user
        card_number=self.cleaned_data.get("cardnumber")
        my_info=MyInformation.objects.filter(user=user).first()
        if my_info.account_number == card_number:
            raise forms.ValidationError("Cannot Send Money from same account to same account")
        return self.cleaned_data
        
        
        
        
        
    
        
        
        
    