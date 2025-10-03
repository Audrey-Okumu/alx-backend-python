from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page   #  added for caching
from .models import Message


@login_required
def delete_user(request):
    """
    View to allow a logged-in user to delete their account.
    """
    user = request.user
    user.delete()   # triggers post_delete signal
    return redirect('/')  # redirect to homepage after deletion


# -------------------------------
#  Threaded conversation helpers
# -------------------------------

def get_thread(message):
    """
    Recursive function to fetch all replies to a message
    and build a threaded structure.
    """
    replies = (
        message.replies.all()
        .select_related("sender", "receiver", "parent_message")
        .order_by("timestamp")
    )
    return [
        {
            "message": reply,
            "replies": get_thread(reply)  # recursion
        }
        for reply in replies
    ]


@login_required
@cache_page(60)   # cache this view for 60 seconds
def threaded_conversation_view(request, user_id):
    """
    Fetch root-level messages between request.user and another user,
    then recursively fetch their replies in a threaded format.
    Cached for 60 seconds.
    """
    root_messages = (
        Message.objects.filter(
            parent_message__isnull=True,
            sender=request.user,
            receiver_id=user_id
        )
        .select_related("sender", "receiver")
        .order_by("timestamp")
    )

    conversation = []
    for msg in root_messages:
        conversation.append({
            "message": msg,
            "replies": get_thread(msg)
        })

    return render(request, "messaging/threaded_conversation.html", {
        "conversation": conversation
    })


# -------------------------------
#  Unread messages inbox view
# -------------------------------

@login_required
def inbox_unread(request):
    """
    Show only unread messages for the logged-in user.
    Uses the custom manager with .only() optimization.
    """
    unread_messages = Message.unread.for_user(request.user)
    return render(request, "messaging/inbox_unread.html", {
        "messages": unread_messages
    })
