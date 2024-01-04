from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('default', views.default, name='default'),
    path('', views.configUpload, name='configUpload'),
    path('welcome', views.welcomePage, name='welcomePage'),
    path('PCAPs', views.PCAPs, name='PCAPs'),
    path('Alerts', views.Alerts, name='Alerts'),
    path('TableBase', views.TableBase, name='TableBase'),
    path('sort', views.sort, name='sort'),
    path('sort', views.sort, name='configComplete'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)