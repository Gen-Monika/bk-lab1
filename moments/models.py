from blueapps.account.models import User
from django.db import models
from django.utils import timezone


class WeChatUser(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    email = models.EmailField(unique=True, null=True)
    motto = models.CharField(max_length=100, null=True, blank=True)
    pic = models.CharField(max_length=50, null=True, blank=True)
    region = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Status(models.Model):
    user = models.ForeignKey(WeChatUser, models.CASCADE, null=True, blank=True)
    chat_user = models.ForeignKey(
        "ChatUser", models.CASCADE, null=True, blank=True, related_name="statuses"
    )
    text = models.CharField(max_length=280)
    pics = models.CharField(max_length=100, null=True, blank=True)
    uploaded_image = models.FileField(upload_to="ciallo_uploads/", null=True, blank=True)
    pub_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    @property
    def author(self):
        return self.chat_user or self.user

    class Meta:
        ordering = ["-id"]


class ChatUser(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password_hash = models.CharField(max_length=128)
    nickname = models.CharField(max_length=40)
    avatar = models.CharField(max_length=120, default="ciallo/characters/murasame.png")
    cover = models.CharField(max_length=120, default="ciallo/bg/clubroom.png")
    bio = models.CharField(max_length=160, blank=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nickname or self.username


class Comment(models.Model):
    status = models.ForeignKey(Status, models.CASCADE, related_name="comments")
    user = models.ForeignKey(ChatUser, models.CASCADE, related_name="comments")
    parent = models.ForeignKey(
        "self", models.CASCADE, null=True, blank=True, related_name="replies"
    )
    text = models.CharField(max_length=180)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.text[:24]}"

    class Meta:
        ordering = ["created_at", "id"]


class Like(models.Model):
    status = models.ForeignKey(Status, models.CASCADE, related_name="likes")
    user = models.ForeignKey(ChatUser, models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} likes {self.status_id}"

    class Meta:
        unique_together = ("status", "user")


class UserActionLog(models.Model):
    blueking_user = models.CharField(max_length=64, blank=True)
    chat_user = models.ForeignKey(
        ChatUser, models.SET_NULL, null=True, blank=True, related_name="action_logs"
    )
    method = models.CharField(max_length=12)
    path = models.CharField(max_length=255)
    status_code = models.PositiveSmallIntegerField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.method} {self.path}"

    class Meta:
        ordering = ["-created_at", "-id"]
