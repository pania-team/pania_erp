from django.urls import path
from . import views



app_name = 'storage'
urlpatterns = [

    path('create-buyinvoice/', views.create_buyinvoice, name='create_buyinvoice'),
    path('buyinvoice-list/', views.buyinvoice_list, name='buyinvoice_list'),
    path('register-buyitem/<int:invoice_id>/', views.register_buyitem, name='register_buyitem'),
    path('storage-list/', views.storage_list, name='storage_list'),
    path('cart-detail/<int:item_id>/', views.cart_detail, name='cart_detail'),

]