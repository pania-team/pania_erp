from django.urls import path
from . import views



app_name = 'sale'
urlpatterns = [
        path('create-goldinvoice/', views.create_goldinvoice, name='create_goldinvoice'),  # مسیر صفحه اول
        path('goldsale_list', views.goldsale_list, name='goldsale_list'),
        path('add-goldinvoice-items/<int:goldinvoice_id>/', views.add_goldinvoice_items, name='add_goldinvoice_items'),
        path('add_goldpayment/<int:goldinvoice_id>/', views.add_goldpayment, name='add_goldpayment'),
        path('goldsale_detail/<int:goldinvoice_id>/', views.goldsale_detail, name='goldsale_detail'),
        path('create-digiinvoice/', views.create_digiinvoice, name='create_digiinvoice'),  # مسیر صفحه اول
        path('digisale_list', views.digisale_list, name='digisale_list'),
        path('add-digiinvoice-items/<int:digiinvoice_id>/', views.add_digiinvoice_items, name='add_digiinvoice_items'),
        path('add_digipayment/<int:digiinvoice_id>/', views.add_digipayment, name='add_digipayment'),
        path('digisale_detail/<int:digiinvoice_id>/', views.digisale_detail, name='digisale_detail'),
        path('pdf-goldsale/<int:invoice_id>/', views.pdf_goldsale_detail, name='pdf_goldsale_detail'),
        path('pdf-digisale/<int:digiinvoice_id>/', views.pdf_digisale_detail, name='pdf_digisale_detail'),


]