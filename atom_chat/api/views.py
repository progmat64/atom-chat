from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from chat.models import Channel, ChannelMembership, Message
from users.models import User

from .serializers import (ChannelSerializer, MessageSerializer,
                          RegistrationSerializer, UserModeratorSerializer,
                          UserPublicSerializer)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = "username"

    def get_serializer_class(self):
        if (
            self.request.user.is_authenticated
            and self.request.user.is_moderator
        ):
            return UserModeratorSerializer
        return UserPublicSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_moderator:
            serializer.validated_data.pop("is_moderator", None)
            serializer.validated_data.pop("is_blocked", None)
        serializer.save()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if not request.user.is_moderator and instance != request.user:
            raise PermissionDenied(
                "У вас нет прав для изменения этого пользователя."
            )

        return super().update(request, *args, **kwargs)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def block(self, request, username=None):
        if not request.user.is_moderator:
            raise PermissionDenied(
                "У вас нет прав для блокировки пользователя."
            )

        user = self.get_object()
        user.is_blocked = True
        user.save()

        return Response(
            {"detail": f"Пользователь {user.username} был заблокирован."},
            status=status.HTTP_200_OK,
        )

    def get_queryset(self):
        queryset = User.objects.all()
        is_blocked = self.request.query_params.get("is_blocked")

        if is_blocked is not None:
            queryset = queryset.filter(is_blocked=is_blocked == "true")

        return queryset


    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.IsAuthenticated],
        url_path='blocked'
    )
    def blocked_users(self, request):
        """Возвращает список заблокированных пользователей для модераторов."""
        if not request.user.is_moderator:
            raise PermissionDenied("У вас нет прав для просмотра заблокированных пользователей.")

        blocked_users = User.objects.filter(is_blocked=True)
        serializer = self.get_serializer(blocked_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        channel = serializer.save(creator=self.request.user)
        ChannelMembership.objects.create(
            user=self.request.user, channel=channel
        )

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def add_user(self, request, pk=None):
        try:
            channel = self.get_object()
        except Channel.DoesNotExist:
            return Response(
                {"detail": "Канал не найден."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.user != channel.creator and not request.user.is_moderator:
            raise PermissionDenied(
                "У вас нет прав для добавления пользователей в этот канал."
            )

        username = request.data.get("username")
        if not username:
            raise ValidationError(
                {"detail": "Необходимо указать имя пользователя."}
            )

        try:
            user_to_add = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"detail": "Пользователь не найден."},
                status=status.HTTP_404_NOT_FOUND,
            )

        ChannelMembership.objects.get_or_create(
            user=user_to_add, channel=channel
        )

        return Response(
            {"detail": f"Пользователь {username} был добавлен в канал."},
            status=status.HTTP_201_CREATED,
        )


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        channel_id = self.kwargs["channel_id"]
        if not ChannelMembership.objects.filter(
            channel_id=channel_id, user=self.request.user
        ).exists():
            raise PermissionDenied("У вас нет доступа к этому каналу.")

        return Message.objects.filter(channel__id=channel_id).order_by(
            "timestamp"
        )

    def perform_create(self, serializer):
        channel_id = self.kwargs["channel_id"]
        try:
            channel = Channel.objects.get(id=channel_id)
        except Channel.DoesNotExist:
            raise ValidationError({"detail": "Канал не найден."})

        if not ChannelMembership.objects.filter(
            channel=channel, user=self.request.user
        ).exists():
            raise PermissionDenied("У вас нет доступа к этому каналу.")

        serializer.save(sender=self.request.user, channel=channel)
