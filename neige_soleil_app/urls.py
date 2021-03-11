from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.accueil, name="accueil"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('home/', views.home_main, name="home_main"),
    path('logout/', views.logoutPage, name="logout"),
    path('profileset/', views.profile_set, name="profile_set"),
    path('new-proprietaire/', views.new_proprietaire, name="new_proprietaire"),
    path('profile-detail/', views.profile_detail, name="profile_detail"),
    path('profile-edit/', views.profile_edit, name="profile_edit"),
    path('proprietaire/', views.proprietaire_main, name="proprietaire"),
    path('new-propriete/', views.new_propriete, name="new_propriete"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('propriete-detail/<str:pk>', views.propriete_detail, name="propriete_detail"),
    path('propriete-edit/<str:pk>', views.edit_propriete, name="propriete_edit"),
    path('reserver/<str:pk>', views.new_reservation, name="reserver"),
    path('louer/<str:pk>', views.louer_propriete, name="louer"),
]
