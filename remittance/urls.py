from django.urls import path
from remittance.views import RemitanceDetailView
app_name="remittance"


urlpatterns = [
    path("details/",RemitanceDetailView.as_view(),name="details")
]
