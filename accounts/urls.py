
from django.urls import path
from . import views



app_name = 'accounts'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('login', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('customer_register/', views.customer_register, name='customer_register'),
    path('customers-with-loans/', views.customers_with_loans, name='customers_with_loans'),

    path('demand_view/', views.demand_view, name='demand_view'),


]



