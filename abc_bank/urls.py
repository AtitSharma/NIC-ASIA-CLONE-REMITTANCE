from django.urls import path
from abc_bank.views import HomeView

app_name="bank"

urlpatterns = [
  path('',HomeView.as_view(),name="home")  
]
