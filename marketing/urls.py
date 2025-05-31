from django.urls import path
from . import views

app_name = 'marketing'
urlpatterns = [
    path('lead_list', views.lead_list, name='lead_list'),
    path('lead_detail/<int:pk>/', views.lead_detail, name='lead_detail'),
    path('lead_create', views.lead_create, name='lead_create'),





]