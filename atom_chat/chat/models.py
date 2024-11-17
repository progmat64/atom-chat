from django.db import models

from users.models import User


class Channel(models.Model):
    name = models.CharField(
        max_length=100, unique=True, verbose_name="Название канала"
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_channel"
    )

    def __str__(self):
        return self.name


class Message(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Содержание")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} in {self.channel}"


class ChannelMembership(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="memberships"
    )
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name="members"
    )

    class Meta:
        unique_together = ("user", "channel")

    def __str__(self):
        return f"{self.user.username} - {self.channel.name}"
