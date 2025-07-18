from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup_user, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:username>/', views.reset_password, name='reset_password'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
