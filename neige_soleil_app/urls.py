from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.accueil, name="accueil"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('home/', views.home_main, name="home_main"),
    path('logout/', views.logoutPage, name="logout"),
    path('profile/', views.profile, name="profile"),
    path('proprietaire/', views.proprietaire_main, name="proprietaire"),
    path('newlocation/', views.new_location, name="new_location"),
    path('reservations/', views.all_reservations, name="reservations"),
    path('locationdetail/<str:pk>', views.location_detail, name="location_detail"),
    path('espace/', views.espace_client, name="espace"),
    path('confirmreserver/', views.confirmReserver, name="confirm_res"),
]
