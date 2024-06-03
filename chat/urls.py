from django.urls import path
from .views import chat_room, get_messages, send_message

app_name = 'chat'

urlpatterns = [
    path('', chat_room, name='chat_room'),  # 기본 URL 패턴
    path('get_messages/', get_messages, name='get_messages'),
    path('send_message/', send_message, name='send_message'),  # 새로운 URL 패턴 추가
]