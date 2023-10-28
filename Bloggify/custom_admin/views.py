# custom_admin/views.py
from django.shortcuts import render

def custom_admin_view(request):
    return render(request, 'custom_admin_page.html')
