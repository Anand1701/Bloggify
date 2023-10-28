"""
URL configuration for Bloggify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from .views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', blog_list.as_view(), name ='home'),
    path('new', what_new.as_view(), name ='new'),
    path('', views.landing, name ='landing'),
    path('signin', views.signin, name = 'signin'),
    path('signup', views.signup, name = 'signup'), 
    path('write_blog',views.write_blog,name='write_blog'),
    path('logout',views.logout,name='logout'),
    path('article/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('edit/<int:pk>/', BlogUpdateView.as_view(), name='update_blog'),
    path('toggle-like/<int:blog_id>/', toggle_like, name='toggle_like'),
    path('userprofile/', userprofile.as_view(), name = 'userprofile'),
    path('editprofile/', views.create_or_update_profile, name = 'editprofile')
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
