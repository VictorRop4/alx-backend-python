from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Prefetch
from .models import Message, User, Conversation
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


@login_required
def delete_user(request):
    user = request.user
    if request.method == 'POST':
        user.delete()  # This will trigger the post_delete signal
        logout(request)  # Log the user out
        messages.success(request, 'Your account and associated data have been deleted.')
        return redirect('home')  # Replace with your homepage URL name
    return redirect('profile')  # Or render a confirmation page before deletion

@login_required
def conversation_detail(request, username):
    user1 = request.user
    user2 = get_object_or_404(User, username=username)

    # Optimized query to get top-level messages with preloaded replies
    messages = Message.objects.filter(
        sender__in=[user1, user2],
        receiver__in=[user1, user2],
        parent_message__isnull=True
    ).select_related('sender', 'receiver').prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
    ).order_by('timestamp')

    context = {
        'other_user': user2,
        'messages': messages,
    }
    return render(request, 'messaging/conversation_detail.html', context)


def get_thread(message):
    """
    Recursively fetch all replies to a message.
    Returns a nested dictionary (or list) representing the message thread.
    """
    replies = message.replies.select_related('sender', 'receiver').all()
    return {
        'message': message,
        'replies': [get_thread(reply) for reply in replies]
    }

@login_required
def unread_messages_view(request):
    user = request.user
    unread_messages = Message.unread.for_user(user)

    context = {
        'unread_messages': unread_messages,
    }
    return render(request, 'messaging/unread_messages.html', context)

@cache_page(60)  # Cache for 60 seconds
def conversation_messages_view(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = Message.objects.filter(conversation=conversation).order_by('timestamp')

    return render(request, 'messaging/conversation_messages.html', {
        'conversation': conversation,
        'messages': messages,
    })