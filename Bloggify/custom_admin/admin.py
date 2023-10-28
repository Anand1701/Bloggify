# custom_admin/admin.py
from django.contrib import admin
from django.urls import path
from Blogapp.models import*
from .views import*
class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('custom-admin/', self.admin_view(custom_admin_view), name='custom-admin'),
        ]
        return custom_urls + urls

custom_admin_site = CustomAdminSite(name='customadmin')

# Register your models with the custom admin site
custom_admin_site.register(Blog)
custom_admin_site.register(AppUsers)
custom_admin_site.register(User)
# Replace YourModel with your actual model

# Now, you can use the custom admin site in place of the default admin site in your project's urls.py
