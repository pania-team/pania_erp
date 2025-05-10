from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls', namespace='accounts')),
    path('demand/', include('demand.urls', namespace='demand')),
    path('sale/', include('sale.urls', namespace='sale')),
    path('reports/', include('reports.urls', namespace='reports')),
    path('finance/', include('finance.urls', namespace='finance')),
    path('taskflow/', include('taskflow.urls', namespace='taskflow')),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)