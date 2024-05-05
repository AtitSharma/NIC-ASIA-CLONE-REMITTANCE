from django import forms
from useraccount.models import PaymentChoices



class UserLoadMoneyForm(forms.Form):
    payment_type=forms.ChoiceField(choices=PaymentChoices.choices)
    amount= forms.DecimalField()
