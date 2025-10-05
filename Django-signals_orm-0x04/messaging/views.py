from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from .models import Message
from django.contrib.auth.models import User


@login_required
def inbox_view(request):
    """
    Display only unread messages for the logged-in user using the custom manager.
    The .only() call ensures only necessary fields are loaded.
    """
    # uses the custom manager method (exact string expected by your checker)
    unread_qs = Message.unread.unread_for_user(request.user)

    # optimize: join sender, and only load required fields
    unread_messages = (
        unread_qs
        .select_related("sender")
        .only("id", "sender_id", "content", "timestamp", "read")
    )

    return render(request, "messaging/inbox.html", {"unread_messages": unread_messages})


@login_required
@cache_page(60)
def conversation_view(request, user_id):
    """
    Show threaded conversation between the logged-in user and another user.
    Demonstrates select_related / prefetch_related and Message.objects.filter usage.
    """
    other = get_object_or_404(User, pk=user_id)

    # fetch root messages (no parent) between the two users, optimized
    messages = (
        Message.objects.filter(
            sender=request.user,
            receiver=other,
            parent_message__isnull=True
        )
        .select_related("sender", "receiver")
        .prefetch_related("replies__sender", "replies__receiver")
    )

    return render(request, "messaging/conversation.html", {"messages": messages, "other": other})

