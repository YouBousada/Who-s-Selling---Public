from messaging.models import MessageModel, ThreadModel

def unread_messages_count(request):
    if request.user.is_authenticated:
        # Get all threads the user is a participant in
        threads = ThreadModel.objects.filter(participants=request.user)
        # Get all messages in those threads that are not read by the user
        # and not sent by the user
        unread_messages_count = MessageModel.objects.filter(
            thread__in=threads
        ).exclude(
            sender_user=request.user
        ).exclude(
            read_by=request.user
        ).count()
        return {'unread_messages_count': unread_messages_count}
    return {}
