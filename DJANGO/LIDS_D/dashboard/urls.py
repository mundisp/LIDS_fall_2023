from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

from .views import get_file_content

urlpatterns = [
    
    
    path('NetworkInfo.html', views.NetworkInfo, name='NetworkInfo'),
    path('viewAlerts.html', views.viewAlerts, name='viewAlerts'),
    path('', views.configServer, name='configServer'),
    path('configComplete.html', views.configComplete, name='configComplete'),
    path('table.html', views.table, name='table'),
    path('alert-detail.html', views.AlertViewset.as_view(), name="alert-detail"),
    path('configServer.html', views.configServer, name='simple_upload'),
    path('get_file_content/', get_file_content, name='get_file_content'),
    

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)