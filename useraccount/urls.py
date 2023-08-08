from django.urls import path
from useraccount.views import LoginUser,RegisterUser,MyprofileView,UserLogout


app_name="user"

urlpatterns = [
    path("login/",LoginUser.as_view(),name="login"),
    path("register/",RegisterUser.as_view(),name="register"),
    path("myprofile/<int:pk>/",MyprofileView.as_view(),name="myprofile"),
    path("logout/",UserLogout.as_view(),name="logout")
]
