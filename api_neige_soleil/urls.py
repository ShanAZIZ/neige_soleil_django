from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_neige_soleil import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'profile', views.ProfileViewSet)
router.register(r'contrat', views.ContratProprietaireViewSet)
router.register(r'reservation', views.ReservationViewSet)


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('token-auth/', views.CustomAuthToken.as_view()),
    path('user-profile/<str:pk>/', views.get_user_profile_view),
    path('user-reservation/<str:pk>/', views.get_user_reservation_view),
    path('user-contrats/<str:pk>/', views.get_contrat_by_user_view),
]
