from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import*
from django.contrib.auth.decorators import login_required
from .models import*
from django.views.generic import ListView, DetailView, UpdateView, TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django import forms


def landing(request):
    return render(request, 'landing.html')
@login_required
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        uname = request.POST['username']
        email = request.POST['email']
        number = request.POST['number']
        pass1 = request.POST['password']
        pass2 = request.POST['cnrf-password']
        
        if pass1 != pass2:
            return HttpResponse("Your password is not matching")
        elif User.objects.filter(username=uname).exists():  
            return HttpResponse("This username is already taken. Please choose another one.")
        elif User.objects.filter(email=email).exists():
            return HttpResponse("Email id is already in use. Try a different email id.")
        else: 
            my_user = User.objects.create_user(uname, email, pass1)
            return redirect('signin')
            
    return render(request, "signup.html") 

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['password']
        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            login(request, user)            
            return redirect('home')
        else:
            return HttpResponse("Username or password is incorrect!!!")

    return render(request, "signin.html")

def logout(request):
    return redirect('landing')

def navbar(request):
    # Assuming you have a user profile linked to the User model
    try:
        profile = AppUsers.objects.get(author=request.user)
    except AppUsers.DoesNotExist:
        profile = None

    context = {
        'user': request.user,
        'profile': profile,
    }

    return render(request, 'base.html', context)

def create_or_update_profile(request):
    try:
        # Check if the user already has a profile
        profile = AppUsers.objects.get(author=request.user)

        # If a profile exists, initialize the form for updating
        form = ProfileForm(instance=profile)
        is_update = True
    except AppUsers.DoesNotExist:
        # If no profile exists, initialize the form for creating
        form = ProfileForm()
        is_update = False

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile if is_update else None)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.author = request.user
            profile.save()
            print("Profile saved successfully!")
            return redirect('userprofile')
        else:
            print("Form errors:", form.errors)

    context = {
        'form': form,
        'is_update': is_update,
    }
    return render(request, 'createprofile.html', context)

    
    
class userprofile(ListView):
    model = Blog
    template_name = 'userprofile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        try:
            profile = AppUsers.objects.get(author=user)
            blog_count = profile
            blogs = context['object_list']  
            context['profile'] = profile
            context['blogs'] = blogs  
        except AppUsers.DoesNotExist:
            profile = None
            blogs = None

        return context


def write_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            
            return redirect('home') 
    else:
        form = BlogForm()
    return render(request, 'write_blog.html', {'form': form})

class blog_list(ListView):
    model = Blog
    template_name = 'home.html'

    def get_queryset(self):

         return Blog.objects.annotate(like_count=Count('likes')).order_by('-like_count')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        blogs = context['object_list']  
        for blog in blogs:

            blog.liked = user.is_authenticated and user in blog.likes.all()

        return context

class what_new(ListView):
    model = Blog
    template_name = 'what_new.html'

    def get_queryset(self):

         return Blog.objects.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        blogs = context['object_list'] 


        for blog in blogs:

            blog.liked = user.is_authenticated and user in blog.likes.all()

        return context
    
class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogs_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.object
        user = self.request.user
        

        context['liked'] = user.is_authenticated and user in blog.likes.all()
        

        context['like_count'] = blog.likes.count()
        
        return context



class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    template_name = "update_blog.html"
    fields = ['title', 'description', 'content', 'image']

    def test_func(self):
        
        blog = self.get_object()
        return self.request.user == blog.author

    def get_success_url(self):
        return reverse_lazy('home')

@login_required
def toggle_like(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
        user = request.user

        if user in blog.likes.all():
            blog.likes.remove(user)
            liked = False
        else:
            blog.likes.add(user)
            liked = True

        like_count = blog.likes.count()
        data = {'liked': liked, 'like_count': like_count}
        return JsonResponse(data)

    except Blog.DoesNotExist:
        return JsonResponse({'error': 'Blog not found'}, status=404)

