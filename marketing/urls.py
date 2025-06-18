from django.urls import path
from . import views

app_name = 'marketing'
urlpatterns = [
    path('leads/', views.lead_list, name='lead_list'),
    path('leads-create/', views.lead_create, name='lead_create'),
    path('leads-detail/<int:pk>/', views.lead_detail, name='lead_detail'),
    path('leads-update/<int:pk>/', views.lead_update, name='lead_update'),
    path('leads-delete/<int:pk>/', views.lead_delete, name='lead_delete'),
    # path('products/', views.product_list, name='product_list'),
    path('products-create/', views.product_create, name='product_create'),
    # path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    # path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('tags-create/', views.tag_create, name='tag_create'),
    path('company-create/', views.company_create, name='company_create'),
]