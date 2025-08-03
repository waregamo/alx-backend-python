from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages as django_messages
from .models import Message
from django.contrib.auth import get_user_model, logout

User = get_user_model()

@login_required
def inbox(request):
    """
    Display top-level messages (no parent) received by the logged-in user.
    Includes sender and receiver info and prefetches replies.
    """
    messages = (
        Message.objects
        .filter(receiver=request.user, parent_message__isnull=True)
        .select_related('sender', 'receiver')
        .prefetch_related('replies')
        .order_by('-timestamp')
    )
    return render(request, 'messaging/inbox.html', {'messages': messages})

@login_required
def view_thread(request, message_id):
    """
    Display a message thread (main message and its replies).
    """
    root_message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver'),
        id=message_id,
        receiver=request.user
    )
    replies = (
        Message.objects
        .filter(parent_message=root_message)
        .select_related('sender', 'receiver')
        .order_by('timestamp')
    )
    return render(request, 'messaging/thread.html', {
        'message': root_message,
        'replies': replies,
    })

@login_required
@require_http_methods(["POST"])
def send_message(request):
    """
    Send a message from the logged-in user to a specified receiver.
    """
    receiver_id = request.POST.get("receiver_id")
    content = request.POST.get("content")
    parent_id = request.POST.get("parent_message_id")

    if receiver_id and content:
        receiver = get_object_or_404(User, id=receiver_id)
        parent_message = Message.objects.filter(id=parent_id).first() if parent_id else None

        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            parent_message=parent_message
        )
        django_messages.success(request, "Message sent successfully.")
    else:
        django_messages.error(request, "Receiver and content are required.")

    return redirect("inbox")

@login_required
@require_http_methods(["POST"])
def delete_user(request):
    """
    Allows the currently logged-in user to delete their own account.
    Related data is cleaned up using a post_delete signal.
    """
    if request.method == "POST":
        user = request.user
        username = user.username
        logout(request)  # Logs out the user before deletion
        user.delete()
        django_messages.success(request, f"User '{username}' and all related data have been deleted.")
        return redirect("home")
