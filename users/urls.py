from django.urls import path
from .views import register_view, login_view, Dashboard, user_logout, display_room


urlpatterns = [
    path('register', register_view, name='registration'),
    path('login', login_view, name='login'),
    path('logout', user_logout, name='logout_user'),
    path('dashboard/<str:pk>', Dashboard.as_view(), name='dashboard'),
    path('space/<str:pk>', display_room)
]
