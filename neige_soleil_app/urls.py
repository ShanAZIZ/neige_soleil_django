from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.accueil, name="accueil"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('home/', views.home_main, name="home_main"),
    path('logout/', views.logoutPage, name="logout"),
    path('proprietaire/', views.proprietaire_main, name="proprietaire"),
    path('newlocation/', views.new_location, name="new_location"),
    path('locationdetail/<str:pk>', views.location_detail, name="location_detail"),
]