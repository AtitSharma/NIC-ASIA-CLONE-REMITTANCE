from django.shortcuts import render,HttpResponseRedirect,redirect
from django.urls import reverse
from django.views import View
from remittance.scraping_data import get_currency_details
from django.contrib.auth.mixins import LoginRequiredMixin
from remittance.forms import UserLoadMoneyForm
from useraccount.models import PaymentChoices,Status
from django.conf import settings
import requests
import json
from remittance.models import TransactionHistory
from django.contrib import messages
from useraccount.models import MyInformation
import uuid

class RemitanceDetailView(View):
    def get(self,request,*args,**kwargs):
        datas=get_currency_details()
        context={
            "datas":datas
        }
        return render(request,"remittance_details.html",context)
    


class LoadMoneyView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        form = UserLoadMoneyForm()
        context = {
            "form":form
        }
        return render(request,"load_money.html",context=context)
    

    def post(self,request,*args,**kwargs):
        user = MyInformation.objects.filter(user=request.user).first()
        if not user:
            messages.add_message(request,messages.INFO,"Create your profile first")
            return redirect(reverse("user:myprofile", kwargs={"pk": request.user.id}))
        if request.POST.get("payment_type")==PaymentChoices.KHALTI.value:
            khalti_initiate_url = settings.KHALTI_INITIATE_URL
            khalti_secret_key = settings.KHATI_SECRET_KEY
            headers = {
            "Authorization": f"key {khalti_secret_key}",
            "Content-Type": "application/json",
            }
            amount =  request.POST.get("amount")
            payload = {
                "return_url":"http://localhost:8000/remittance/khalti/",
                "website_url":"http://localhost:8000/",
                "amount":float(amount)*100,
                "purchase_order_id":request.user.id,
                "purchase_order_name":request.user.id
            }
            payload = json.dumps(payload)
            response = requests.request("POST", khalti_initiate_url, headers=headers, data=payload)
            if response.status_code == 200:
                response = response.json()
                TransactionHistory.objects.create(user=request.user,
                                                amount=amount,status=Status.INITIATE,transaction_id=response.get("pidx"),
                                                transaction_response= response,
                                                transaction_type=PaymentChoices.KHALTI)
                payment_url = response.get("payment_url")
                return HttpResponseRedirect(redirect_to=payment_url)
        if request.POST.get("payment_type")==PaymentChoices.ESEWA.value:
            transaction_id = str(uuid.uuid4())
            amount =  request.POST.get("amount")
            TransactionHistory.objects.create(user=request.user,
                                                amount=amount,status=Status.INITIATE,transaction_id=transaction_id,
                                                transaction_response= {},
                                                transaction_type=PaymentChoices.ESEWA)
            context = {
                "transaction_id":transaction_id,
                "amount":amount,
                "secret":"EPAYTEST",
                "su":f"http://localhost:8000/remittance/esewa-su/?id={transaction_id}",
                "fu":f"http://localhost:8000/remittance/esewa-fu/?id={transaction_id}"
            }
            return render(request,"esewa.html",context=context)



class KhatiAfterPaymentView(View):

    def get(self,request,*args,**kwargs):
        form = UserLoadMoneyForm()
        context = {
            "form":form
        }
        khalti_response = request.GET
        status = khalti_response.get("status")
        if status.lower() == "completed":
            pidx = khalti_response.get("pidx")
            transaction= TransactionHistory.objects.filter(transaction_id=pidx).first()
            if not transaction:
                messages.add_message(request,messages.INFO,"Your Transaction is failed")
                return render(request,"load_money.html",context=context)
            khalti_lookup_url = settings.KHALTI_LOOK_URL
            secret_key = settings.KHATI_SECRET_KEY
            headers = {"Authorization": f"key {secret_key}"}
            payload = {
                "pidx": pidx,
                }
            response = requests.request("POST", khalti_lookup_url, headers=headers, data=payload)
            if response.status_code == 200 :
                status = response.json().get("status")
                if status.lower() == "completed":
                    transaction.transaction_response = khalti_response
                    transaction.status = Status.SUCCESS
                    transaction.save()
                    transaction.user.profile.amount += transaction.amount
                    transaction.user.profile.save()
                    messages.add_message(request,messages.INFO,"Your Transaction is completed Successfully")
            
            return render(request,"load_money.html",context=context)
        messages.add_message(request,messages.INFO,"Your Transaction is failed")
        return render(request,"load_money.html",context=context)
        
        
class EsewaAfterPaymentSuccessView(View):
    def get(self,request,*args,**kwargs):

        form = UserLoadMoneyForm()
        context = {
            "form":form
        }

        response = request.GET
        transaction = TransactionHistory.objects.filter(transaction_id=response.get("id")).first()
        if not transaction:
            messages.add_message(request,messages.INFO,"Your Transaction is failed")
            return render(request,"load_money.html",context=context)
        transaction.status = Status.SUCCESS
        transaction.save()
        transaction.user.profile.amount += transaction.amount
        transaction.user.profile.save()
        messages.add_message(request,messages.INFO,"Your Transaction is completed Successfully")
        return render(request,"load_money.html",context=context)


class EsewaAfterPaymentFailView(View):
    def get(self,request,*args,**kwargs):
        form = UserLoadMoneyForm()
        context = {
            "form":form
        }

        response = request.GET
        transaction = TransactionHistory.objects.filter(transaction_id=response.get("id")).first()
        if not transaction:
            messages.add_message(request,messages.INFO,"Your Transaction is failed")
            return render(request,"load_money.html",context=context)
        transaction.status = Status.FAIL
        transaction.transaction_response = response
        transaction.save()
        messages.add_message(request,messages.INFO,"Your Transaction is failed")
        return render(request,"load_money.html",context=context)
