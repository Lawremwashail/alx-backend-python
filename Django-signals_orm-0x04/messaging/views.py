from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Message



@login_required
def delete_user(request):
    """
    View that allows a logged-in user to delete their own account.
    """
    user = request.user
    user.delete()
    return redirect("login")  # redirect to login page after deletion


@login_required
def conversation_view(request, user_id):
    """
    Show threaded conversation between the logged-in user and another user.
    Optimized with select_related and prefetch_related.
    """
    # Fetch all top-level messages (no parent) between two users
    messages = (
        Message.objects.filter(sender=request.user, receiver_id=user_id, parent_message__isnull=True)
        .select_related("sender", "receiver")
        .prefetch_related("replies__sender", "replies__receiver")
    )


@login_required
def inbox_view(request):
    unread_messages = Message.unread.for_user(request.user)
    return render(request, "messaging/inbox.html", {"unread_messages": unread_messages})
