from django.urls import path
from remittance.views import (RemitanceDetailView,
                              LoadMoneyView,KhatiAfterPaymentView,
                              EsewaAfterPaymentSuccessView,EsewaAfterPaymentFailView)
app_name="remittance"


urlpatterns = [
    path("details/",RemitanceDetailView.as_view(),name="details"),
    path("load-money/",LoadMoneyView.as_view(),name="load-money"),
    path("khalti/",KhatiAfterPaymentView.as_view(),name="khalti"),
    path("esewa-su/",EsewaAfterPaymentSuccessView.as_view(),name="esewa-su"),
    path("esewa-fu/",EsewaAfterPaymentFailView.as_view(),name="esewa-fu"),
]
