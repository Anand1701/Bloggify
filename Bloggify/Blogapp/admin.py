from django.contrib import admin

# Register your models here.
from .models import*


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'author', 'created_at')

@admin.register(AppUsers)
class AppUsersAdmin(admin.ModelAdmin):
    list_display = ('author', 'first_name', 'last_name', 'email', 'dob', 'gender', 'blog_count')