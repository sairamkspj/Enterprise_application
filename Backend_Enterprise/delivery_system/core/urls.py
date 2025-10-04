from django.urls import path
from .views import Registration,login_user


urlpatterns=[
    path('register/',Registration,name="register"),
    path('login_user/',login_user,name="login_user")
]