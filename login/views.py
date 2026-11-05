from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.views import View
from django.utils.decorators import method_decorator

def login_view(request):
    if request.user.is_authenticated:
        return redirect('marketplace')
     
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('login:post_login_redirect')
        else:
            return HttpResponse("Invalid username or password.")
   
    return render(request, "login/login.html")

@login_required
def post_login_redirect(request):
    if request.user.profile.is_new_user:
        return redirect('login:intro')
    else:
        return redirect('marketplace')





from items.forms import ProfileForm

from items.models import Post

@method_decorator(login_required, name='dispatch')
class DeleteAccountView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        # Delete all posts by the user
        Post.objects.filter(user=user).delete()
        logout(request)
        user.delete()
        return redirect('account_login')

@method_decorator(login_required, name='dispatch')
class IntroView(View):
    def get(self, request, *args, **kwargs):
        form = ProfileForm(instance=request.user.profile)
        return render(request, 'login/intro.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.is_new_user = False
            profile.save()
            return redirect('marketplace')
        return render(request, 'login/intro.html', {'form': form})




