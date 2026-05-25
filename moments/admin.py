from django.contrib import admin

from .models import ChatUser, Comment, Like, Status, UserActionLog, WeChatUser


@admin.register(ChatUser)
class ChatUserAdmin(admin.ModelAdmin):
    list_display = ("username", "nickname", "is_admin", "created_at")
    search_fields = ("username", "nickname")
    list_filter = ("is_admin",)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("id", "chat_user", "user", "text", "pub_time")
    search_fields = ("text", "chat_user__username", "chat_user__nickname")
    list_filter = ("pub_time",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "user", "text", "created_at")
    search_fields = ("text", "user__username", "user__nickname")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "user", "created_at")
    search_fields = ("user__username", "user__nickname")


@admin.register(UserActionLog)
class UserActionLogAdmin(admin.ModelAdmin):
    list_display = ("method", "path", "status_code", "blueking_user", "chat_user", "created_at")
    search_fields = ("path", "blueking_user", "chat_user__username")
    list_filter = ("method", "status_code", "created_at")


admin.site.register(WeChatUser)
