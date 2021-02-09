from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.accueil, name="accueil"),
    path('/register', views.register, name="register"),
    path('/login', views.loginPage, name="login"),
    path('/home', views.home_main, name="home_main"),
]