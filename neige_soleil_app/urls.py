from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.accueil, name="accueil"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('home/', views.main_home, name="main_home"),
    path('logout/', views.logoutPage, name="logout"),
    path('profileset/', views.new_profile, name="new_profile"),
    path('new-proprietaire/', views.new_proprietaire, name="new_proprietaire"),
    path('profile-detail/', views.detail_profile, name="detail_profile"),
    path('profile-edit/', views.edit_profile, name="edit_profile"),
    path('password-edit/', views.edit_password, name="edit_password"),
    path('proprietaire/', views.main_proprietaire, name="main_proprietaire"),
    path('new-propriete/', views.new_propriete, name="new_propriete"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('propriete-detail/<str:pk>', views.detail_propriete, name="detail_propriete"),
    path('propriete-edit/<str:pk>', views.edit_propriete, name="propriete_edit"),
    path('reserver/<str:pk>', views.new_reservation, name="reserver"),
    path('edit-reservation/<str:pk>', views.edit_reservation, name="edit_reservation"),
    path('louer/<str:pk>', views.new_location, name="louer"),
]
