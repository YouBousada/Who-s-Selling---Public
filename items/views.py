from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from .forms import ProfileForm
from .models import Post, Category
from django.http import HttpResponseForbidden
from .forms import PostForm
from django.contrib.auth.decorators import login_required 
from django.db.models import Max
from django.contrib.auth.models import User
from login.models import Profile
from django.contrib import admin
from .models import Category
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth import logout




@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if post.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")
    
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully!")
    
        return redirect("marketplace")  


def marketplace(request):
    posts = Post.objects.all()

    keyword = request.GET.get('keyword', '')
    category = request.GET.get('category', '')
    max_price = request.GET.get('price', '')

    if keyword:
        posts = posts.filter(title__icontains=keyword) | posts.filter(description__icontains=keyword)

    if category:
        posts = posts.filter(category__name__iexact=category)

    if max_price:
        try:
            posts = posts.filter(asking_price__lte=float(max_price))
        except ValueError:
            pass
    
    categories = Category.objects.all()

    max_asking_price = Post.objects.aggregate(Max('asking_price'))['asking_price__max'] or 500

    context = {
        'posts': posts,
        'keyword': keyword,
        'category': category,
        'price': max_price,
        'categories': categories,
        'max_asking_price': int(max_asking_price),
    }
    return render(request, 'marketplace.html', context)

def userpage(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    posts = Post.objects.filter(user=user)
    
    display_name = profile.nickname if profile.nickname else user.username
    
    context = {
        'user': user,
        'profile': profile,
        'posts': posts,
        'display_name': display_name
    }
    return render(request, 'profile.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():

            post = form.save(commit=False)
            post.user = request.user  
            post.save()

            success_message = "Your post has been uploaded successfully!"
            return render(request, 'createPost.html', {'form': form, 'success_message': success_message})

    else:
        form = PostForm()

    return render(request, 'createPost.html', {'form': form})


def view_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post.html', {'post': post})

@login_required
def editprofile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('userpage', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    
    display_name = profile.nickname if profile.nickname else request.user.username
    
    return render(request, 'editProfile.html', {'form': form, 'display_name': display_name}) 


def logout_view(request):
    logout(request) 
    return redirect('login') 


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if not request.user.is_superuser and post.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()  
            messages.success(request, "Your post has been updated successfully!")
            return redirect("view_post", post_id=post.id)  
    else:
        form = PostForm(instance=post)

    return render(request, "editpost.html", {"form": form})


