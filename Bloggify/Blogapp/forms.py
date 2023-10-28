from django import forms
from .models import Blog, AppUsers

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description', 'content', 'image']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = AppUsers
        fields = ['first_name', 'last_name', 'dob', 'email', 'profile_pic', 'cover', 'gender']
