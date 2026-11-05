from django.urls import path
from .views import CreateThread, ListThreads, ThreadView, CreateMessage, UserSearchView, UnreadMessagesCountView

app_name = "messaging"

urlpatterns = [
    path('inbox/', ListThreads.as_view(), name = 'inbox'),
    path('inbox/create-thread', CreateThread.as_view(), name = 'create-thread'),
    path('inbox/<int:pk>/', ThreadView.as_view(), name = 'thread'), 
    path('inbox/<int:pk>/create-message/', CreateMessage.as_view(), name = 'create-message'),
    path('inbox/search-users/', UserSearchView.as_view(), name='search-users'),
    path('inbox/unread-count/', UnreadMessagesCountView.as_view(), name='unread-count'),
]