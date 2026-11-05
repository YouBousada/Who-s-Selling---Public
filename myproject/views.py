from django.http import HttpResponse
from django.contrib import admin
from django.urls import path

def home(request):
    return HttpResponse("Welcome to our Django project from team B-22! There's not much to see here yet but just wait.")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
]