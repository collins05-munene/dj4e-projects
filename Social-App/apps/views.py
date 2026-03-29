from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from .forms import UserRegistrationForm, ClientUpdateForm, UserUpdateForm, PostForm, CommentForm
from django.contrib import messages
from .models import Client, Comment, Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


# Create your views here.
User = get_user_model()

class Homepage(View):
    def get(self, request):
        context = {}
        return render(request, 'apps/home.html', context)
    
class CustomRegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        context = {
            'form': form
        }
        return render(request, 'apps/create-user.html', context)
    
    def post(self, request):
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                messages.error(request, 'Password mismatch')
                return redirect('register-user')
            if User.objects.filter(username=username).exists():
                messages.error(request, f'{username} already exists')

            user = User.objects.create_user(username=form.cleaned_data['username'])
            user.set_password(password)
            user.save()

            client = form.save(commit=False)
            client.user = user
            client.save()

            return redirect('login')
        context = {
            'form': form
        }
        return render(request, 'apps/create-user.html', context)
    

class CustomLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        context = {
            'form': form
        }
        return render(request, 'apps/login.html', context)
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request, user)
            if user.is_active:
                return redirect('client-page')
        else:
            context = {
                'error': 'Invalid Credentials'
            }
            return render(request, 'apps/login.html', context)

class ClientPage(LoginRequiredMixin, View):
    def get(self, request):
        posts = Post.objects.all().prefetch_related('likes').order_by('-updated_at')
        for post in posts:
            post.is_liked = request.user in post.likes.all()

        context = {'posts': posts}
        return render(request, 'apps/client-page.html', context)
    
class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'apps/delete-account.html'
    success_url = reverse_lazy('homepage')
    
    def get_object(self):
        return self.request.user
    def delete(self, request, *args, **kwargs):
        logout(request)
        return super().delete(request, *args, **kwargs)
    
class ClientUpdateView(LoginRequiredMixin, View):
    template_name = 'apps/update-client.html'
    def get(self, request):
        client, _ = Client.objects.get_or_create(user=request.user)

        client_form = ClientUpdateForm(instance=client)
        user_form = UserUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)
        context = {
            'client_form': client_form,
            'user_form': user_form,
            'password_form': password_form
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        client, _ = Client.objects.get_or_create(user=request.user)

        client_form = ClientUpdateForm(request.POST, instance=client)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if 'update_profile' in request.POST:
            if client_form.is_valid()  and user_form.is_valid():
                client_form.save()
                user_form.save()
                messages.success(request, 'Profile updated successfully')
                return redirect('client-page')
        elif 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user) #Keep user logged in
                messages.success(request, "Password Updated successfully")
                return redirect('client-page')
        
        context = {
            'client_form': client_form,
            'user_form': user_form,
            'password_form': password_form
            }
        return render(request, self.template_name, context)
    
class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('login')

class PostCreateView(LoginRequiredMixin, View):
    template_name = 'apps/create-post.html'

    def get(self, request):
        form = PostForm()
        context = {'form': form}
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully')
            return redirect('client-page')
        context = {'form': form}
        return render(request, self.template_name, context)
        

class PostUpdateView(View):
    template_name = 'apps/update_post.html'

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            messages.error(request, 'You are not allowed to perform the following operations')
            return redirect('client-page')
        
        form = PostForm(instance=post)
        context = {'form': form, 'post': post}
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        if post.author != request.user:
            messages.error(request, 'You are not allowed the following operations')
            return redirect('client-page')

        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully')
            return redirect('client-page')
        
        context = {'form': form, 'post': post}
        return render(request, self.template_name, context)

class PostDeleteView(LoginRequiredMixin, View):
    template_name = 'apps/delete-post.html'

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
            
        if post.author != request.user:
            messages.error(request, 'Restricted')
            return redirect('client-page')
        
        context = {'post': post}
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            messages.error(request, 'Restricted')
            return redirect('client-page')
        post.delete()
        messages.success(request, 'Post deleted successfully')
        return redirect('client-page')

class CommentCreateView(LoginRequiredMixin, View):
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)

        parent_id = request.POST.get('parent_id')

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post

            #reply
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
                comment.parent = parent_comment

            comment.save()

        return redirect('post-detail', pk=post.pk)
    
class PostDetailView(View):
    template_name = 'apps/post-detail.html'

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        is_liked = request.user in post.likes.all()

        comments = post.comments.filter(parent__isnull=True)

        form = CommentForm()
        context = {
            'post': post, 'comments':comments, 'form': form, 'is_liked': is_liked
        }
        return render(request, self.template_name, context)
    
class ToggleLikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return redirect('client-page')