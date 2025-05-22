from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('get-month-stats/', views.get_month_stats, name='get_month_stats'),
    path('get-stats/', views.get_stats, name='get_stats'),
    path('profile-stats/', views.profile_stats, name='profile_stats'),
] 