from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from useraccount.models import MyInformation
from payments.forms import CashTransferForm
from django.contrib import messages
from payments.models import PaymentHistory

class CheckOutView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwars):
        my_info=MyInformation.objects.filter(user__id=request.user.id).first()
        context={
            "info":my_info
        }
        return render(request,"checkout.html",context)
        

    
    def post(self,request,*args,**kwargs):
        form=CashTransferForm(request.POST,request=request)
        if form.is_valid():
            my_info=MyInformation.objects.filter(user=request.user).first()
            creditor_bank=my_info.account_number
            debtors_bank=request.POST.get("cardnumber")
            debtor_user=MyInformation.objects.filter(account_number=debtors_bank).first().user
            debtor_info=MyInformation.objects.filter(user=debtor_user).first()
            amount=int(request.POST.get("amount"))
            PaymentHistory.objects.create(user=my_info.user,from_account=creditor_bank,amount=f"-{amount}",to_account=debtors_bank,status="debit")
            PaymentHistory.objects.create(user=debtor_user,from_account=creditor_bank,amount=f"+{amount}",to_account=debtors_bank,status="credit")
            my_info.amount-=amount
            debtor_info.amount+=amount
            my_info.save()
            debtor_info.save()
            messages.add_message(request,messages.INFO,"Successfully Transferred the Cash ")
            return redirect("bank:home")

        
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.add_message(request, messages.ERROR, f"{error}")
        return redirect(request.META.get("HTTP_REFERER"))
    
    
    
    

class HistoryView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        histories=PaymentHistory.objects.filter(user=request.user).order_by("-transation_date")
        context={
            "histories":histories
        }
        return render(request,"history.html",context)
    
    
    


