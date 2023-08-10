from payments.views import CheckOutView,HistoryView
from django.urls import path

app_name="pay"

urlpatterns = [
    path("checkout/",CheckOutView.as_view(),name="checkout"),
    path("history/",HistoryView.as_view(),name="history")
]

