from django.urls import path
from . import views



app_name = 'finance'
urlpatterns = [
        path('list_payments', views.list_payments, name='list_payments'),
        path('list_appro_payments', views.list_appro_payments, name='list_appro_payments'),
        path('add_goldpayment_reciept/<int:payments_id>/', views.add_goldpayment_reciept, name='add_goldpayment_reciept'),
        path('list_digipayments', views.list_digipayments, name='list_digipayments'),
        path('list_appro_digipayments', views.list_appro_digipayments, name='list_appro_digipayments'),
        path('add_digipayment_reciept/<int:payments_id>/', views.add_digipayment_reciept, name='add_digipayment_reciept'),


]