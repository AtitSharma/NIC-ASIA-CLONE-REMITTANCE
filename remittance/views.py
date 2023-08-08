from django.shortcuts import render
from django.views import View
from remittance.scraping_data import get_currency_details


class RemitanceDetailView(View):
    def get(self,request,*args,**kwargs):
        datas=get_currency_details()
        context={
            "datas":datas
        }
        return render(request,"remittance_details.html",context)
        
        
        