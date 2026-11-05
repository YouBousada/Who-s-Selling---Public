from django.urls import path
from . import views

urlpatterns = [
    path('create_post/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('user/<str:username>/', views.userpage, name='userpage'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('post/<int:post_id>/', views.view_post, name='view_post'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('logout/', views.logout_view, name='logout'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
]
