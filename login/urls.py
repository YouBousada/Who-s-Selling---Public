from django.urls import path
from .views import DeleteAccountView, IntroView, post_login_redirect
from django.contrib.auth.views import LogoutView

app_name = 'login'

urlpatterns = [
    path('delete_account/', DeleteAccountView.as_view(), name='delete_account'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('intro/', IntroView.as_view(), name='intro'),
    path('post_login_redirect/', post_login_redirect, name='post_login_redirect'),
]
