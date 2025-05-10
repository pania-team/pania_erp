from django.urls import path
from . import views



app_name = 'reports'
urlpatterns = [
    path('goldreport_list/', views.goldreport_list, name='goldreport_list'),

]