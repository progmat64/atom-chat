# asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Установка DJANGO_SETTINGS_MODULE для инициализации настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "atom_chat.settings")

# Инициализация приложения Django перед импортом зависимых модулей
django_asgi_app = get_asgi_application()

# Теперь импортируем JWTAuthMiddleware и маршруты WebSocket
from chat.middleware import JWTAuthMiddleware
import chat.routing

# Определение ProtocolTypeRouter с http и websocket протоколами
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        )
    ),
})
