from django.urls import path, include
from .views import RegisterView, LoginView, UserView, LogoutView, ForgotPasswordView, ResetPasswordView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forgotpassword/', ForgotPasswordView.as_view(), name='forgotpassword'),
    path('resetpassword/<uidb64>/<token>/', ResetPasswordView.as_view(), name='resetpassword'),
    path('resetpassword/', ResetPasswordView.as_view(), name='resetpasswordconfirmed'),
]