from django.urls import path
from abc_bank.views import HomeView,SupportView

app_name="bank"

urlpatterns = [
  path('',HomeView.as_view(),name="home")  ,
  path("support/",SupportView.as_view(),name="support")
]
