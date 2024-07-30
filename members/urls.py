from django.urls import path, include
from .views import RegisterView, LoginView, UserView, LogoutView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('api/register', RegisterView.as_view(), name='register_api'),
    path('api/login', LoginView.as_view(), name='login_api'),
    path('api/logout', LogoutView.as_view(), name='logout'),
    path('api/user', UserView.as_view(), name='user'),
]