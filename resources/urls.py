from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    path('', views.resource_list, name='resource_list'),
    path('add/', views.resource_add, name='resource_add'),
    path('edit/<int:pk>/', views.resource_edit, name='resource_edit'),
    path('delete/<int:pk>/', views.resource_delete, name='resource_delete'),
    path('comment/<int:resource_id>/', views.add_comment, name='add_comment'),
    path('detail/<int:pk>/', views.resource_detail, name='resource_detail'),
] 