from django.contrib import admin

from .models import Status, WeChatUser


admin.site.register(WeChatUser)
admin.site.register(Status)
