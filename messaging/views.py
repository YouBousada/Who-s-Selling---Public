from django.shortcuts import redirect, render
from django.views import View
from django.db.models import Q
from django.db import models

from messaging.forms import MessageForm, ThreadForm
from messaging.models import MessageModel, ThreadModel
from login.models import Profile

from django.contrib.auth.models import User

# Create your views here.

class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(participants=request.user)
        thread_list = []
        for thread in threads:
            unread_count = MessageModel.objects.filter(
                thread=thread
            ).exclude(
                sender_user=request.user
            ).exclude(
                read_by=request.user
            ).count()
            
            other_participants = thread.participants.exclude(id=request.user.id)
            profiles = [Profile.objects.get(user=p) for p in other_participants]
            thread_list.append({
                'thread': thread,
                'participant_profiles': profiles,
                'unread_count': unread_count
            })

        context = {
            'thread_list': thread_list
        }
        return render(request, 'messaging/inbox.html', context)
    
class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()

        context = {
            'form': form
        }
        return render(request, 'messaging/create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        if form.is_valid():
            participants = form.cleaned_data['participants']
            if len(participants) > 6:
                return redirect('messaging:create-thread')

            all_participants = list(participants) + [request.user]
            
            threads = ThreadModel.objects.annotate(num_participants=models.Count('participants')).filter(num_participants=len(all_participants))
            for p in all_participants:
                threads = threads.filter(participants=p)
            
            if threads.exists():
                return redirect('messaging:thread', pk=threads.first().pk)

            thread = ThreadModel.objects.create()
            thread.participants.set(all_participants)
            return redirect('messaging:thread', pk=thread.pk)
        
        return redirect('messaging:create-thread')
        
class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread=thread)
        
        # Mark messages as read
        for message in message_list:
            message.read_by.add(request.user)

        participants = thread.participants.all()
        participant_profiles = [Profile.objects.get(user=p) for p in participants]

        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list,
            'participant_profiles': participant_profiles,
        }
        return render(request, 'messaging/thread.html', context)

class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        thread = ThreadModel.objects.get(pk=pk)
        message = MessageModel(
            thread=thread,
            sender_user=request.user,
            body=request.POST.get('message')
        )
        message.save()
        return redirect('messaging:thread', pk=pk)
    
from django.http import JsonResponse
class UnreadMessagesCountView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'unread_messages_count': 0})

        threads = ThreadModel.objects.filter(participants=request.user)
        unread_messages_count = MessageModel.objects.filter(
            thread__in=threads
        ).exclude(
            sender_user=request.user
        ).exclude(
            read_by=request.user
        ).count()
        return JsonResponse({'unread_messages_count': unread_messages_count})

class UserSearchView(View):
    def get(self, request, *args, **kwargs):
        term = request.GET.get('term', '')
        # Exclude the current user from the search results
        users = User.objects.filter(
            Q(username__icontains=term) | Q(profile__nickname__icontains=term)
        ).exclude(id=request.user.id)
        results = []
        for user in users:
            display_text = user.username
            if hasattr(user, 'profile') and user.profile.nickname:
                display_text = f"{user.profile.nickname} ({user.username})"
            results.append({
                'id': user.id,
                'text': display_text
            })
        return JsonResponse({'results': results})