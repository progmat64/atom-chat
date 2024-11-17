from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ChannelViewSet, MessageListCreateView, RegisterView, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"channels", ChannelViewSet, basename="channel")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("", include(router.urls)),
    path(
        "channels/<int:channel_id>/messages/",
        MessageListCreateView.as_view(),
        name="message-list-create",
    ),
]
