from django.urls import path
from .views import chat_room, get_messages

app_name = 'chat'

urlpatterns = [
    path('', chat_room, name='chat_room'),  # 기본 URL 패턴
    path('get_messages/', get_messages, name='get_messages'),
]