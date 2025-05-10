from django.urls import path
from . import views



app_name = 'demand'
urlpatterns = [
    path('demand/',views.demand, name='demand'),
    path('demand_remain/',views.demand_remain, name='demand_remain'),
    path('demand_vosoli/',views.demand_vosoli, name='demand_vosoli'),
    path('loan_list', views.loan_list, name='loan_list'),
    path('export-loans/', views.export_loans_excel, name='export_loans_excel'),

    path('loan_detail/<int:loan_id>/', views.loan_detail, name='loan_detail'),
    path('loan/<int:loan_id>/update-installments/', views.update_installments, name='update_installments'),
    path('loan/<int:loan_id>/create_installments/', views.create_installments, name='create_installments'),
    path('create_repayment/<int:installment_id>/', views.create_repayment, name='create_repayment'),
    path('create_loan/', views.create_loan, name='create_loan'),
    path('create_zemanat/<int:loan_id>/', views.create_zemanat, name='create_zemanat'),
    path('pdf-loan/<int:loan_id>/', views.pdf_loan_agreement, name='pdf_loan_agreement'),
    path('pdf-loanduc/<int:loan_id>/', views.pdf_loan_document, name='pdf_loan_document'),
    # path('calculate-penalty/<int:installment_id>/', views.calculate_penalty, name='calculate_penalty'),
]