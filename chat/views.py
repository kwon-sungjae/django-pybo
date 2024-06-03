from django.shortcuts import render, get_object_or_404
from .models import ChatRoom, Message
from .forms import MessageForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.middleware.csrf import get_token

@login_required(login_url='common:login')
def chat_room(request):
    room = get_object_or_404(ChatRoom, name='test')
    messages = Message.objects.filter(room=room).order_by('timestamp')
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            Message.objects.create(room=room, user=request.user, content=content)
            # 저장 후 어떤 동작을 수행하거나 리다이렉트할 수 있습니다.
    else:
        form = MessageForm()
    
    context = {
        'room': room,
        'messages': messages,
        'form': form,
    }
    return render(request, 'chat/chat_room.html', context)

@login_required(login_url='common:login')
def get_messages(request):
    room = get_object_or_404(ChatRoom, name='test')
    messages = Message.objects.filter(room=room).order_by('timestamp')
    messages_data = [{
        'user': message.user.username,
        'content': message.content,
        'timestamp': message.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    } for message in messages]
    return JsonResponse({'messages': messages_data})

@login_required(login_url='common:login')
@require_POST
def send_message(request):
    room = get_object_or_404(ChatRoom, name='test')
    content = request.POST.get('content', None)
    if content:
        # 채팅 메시지를 저장
        message = Message.objects.create(room = room, content=content, user=request.user)
        # 새로운 메시지의 정보를 반환
        message_data = {
            'user': message.user.username,
            'content': message.content,
            'timestamp': message.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        # CSRF 토큰을 가져와서 JSON 응답에 추가
        csrf_token = get_token(request)
        response_data = {'message': message_data, 'csrf_token': csrf_token}
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'No content provided'}, status=400)

