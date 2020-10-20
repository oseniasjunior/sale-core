from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from core import consumers

urlrouter = [
    path('chat/', consumers.ChatConsumer),
]

application = ProtocolTypeRouter({
    "websocket": URLRouter(urlrouter)
})
