from django.conf import settings
from django.shortcuts import redirect, render

from .models import Status, WeChatUser


def home(request):
    return render(request, "moments/homepage.html")


def show_user(request):
    user_id = request.user.id
    wechat_user = WeChatUser.objects.get(user_id=user_id)
    return render(request, "moments/user.html", {"user": wechat_user})


def show_status(request):
    statuses = Status.objects.all()
    return render(request, "moments/status.html", {"statuses": statuses})


def submit_post(request):
    user = WeChatUser.objects.get(user=request.user)
    text = request.POST.get("text")
    if text:
        status = Status(user=user, text=text)
        status.save()
        return redirect(f"{settings.SITE_URL}status/")
    return render(request, "moments/my_post.html")
