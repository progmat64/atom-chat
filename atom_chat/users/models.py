from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        max_length=254, unique=True, verbose_name="Почта"
    )
    username = models.CharField(
        max_length=150, unique=True, verbose_name="Имя пользователя"
    )
    first_name = models.CharField(max_length=150, verbose_name="Имя")
    last_name = models.CharField(max_length=150, verbose_name="Фамилия")
    password = models.CharField(max_length=150, verbose_name="Пароль")

    is_moderator = models.BooleanField(default=False, verbose_name="Модератор")
    is_blocked = models.BooleanField(
        default=False, verbose_name="Заблокирован"
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name", "password"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    # def save(self, *args, **kwargs):
    #     # Хэшируем пароль только если пользователь не является суперпользователем
    #     if not self.is_superuser and not self._state.adding:
    #         raw_password = self.password
    #         self.set_password(raw_password)
    #     super().save(*args, **kwargs)
