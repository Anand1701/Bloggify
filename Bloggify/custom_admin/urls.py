from django.contrib import admin
from django.urls import include, path
from .views import*


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Blogapp.urls')),
    path('custom-admin/', custom_admin_view, name='custom-admin'),
    
]