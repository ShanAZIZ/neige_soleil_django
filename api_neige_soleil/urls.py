from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_neige_soleil import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'profile', views.ProfileViewSet)
router.register(r'reservation', views.ReservationViewSet)
router.register(r'location', views.LocationViewSet)


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('api/', include(router.urls)),
    path('api-token-auth/', views.CustomAuthToken.as_view()),
    path('api/user-profile/<str:pk>/', views.getUserProfileView.as_view()),
]
