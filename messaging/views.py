from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

@login_required
def inbox(request):
    unread_msgs = Message.unread.for_user(request.user)
    return render(request, 'messaging/inbox.html', {'unread_messages': unread_msgs})

@login_required
@cache_page(60)
def view_thread(request, message_id):
    root = get_object_or_404(
        Message.objects.select_related('sender', 'receiver'),
        pk=message_id, receiver=request.user
    )
    replies = root.replies.select_related('sender', 'receiver').all().order_by('timestamp')
    edit_history = root.edit_history.order_by('-edited_at')
    return render(request, 'messaging/thread.html', {
        'message': root,
        'replies': replies,
        'edit_history': edit_history
    })

@login_required
def send_message(request):
    if request.method == 'POST':
        recv = get_object_or_404(User, pk=request.POST.get('receiver_id'))
        parent = Message.objects.filter(pk=request.POST.get('parent_message_id')).first()
        Message.objects.create(sender=request.user, receiver=recv, content=request.POST.get('content'), parent_message=parent)
        return redirect('inbox')
    users = User.objects.exclude(pk=request.user.pk)
    return render(request, 'messaging/send.html', {'users': users})

@login_required
def delete_user(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('home')
    return render(request, 'messaging/confirm_delete.html')
