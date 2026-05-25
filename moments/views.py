from django.contrib import messages
from django.db.models import Prefetch
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .assets import AVATAR_CHOICES, BACKGROUND_CHOICES
from .forms import CommentForm, LoginForm, ProfileForm, RegisterForm, StatusForm
from .models import Comment, Like, Status
from .services import get_current_chat_user, login_chat_user, logout_chat_user


def home(request):
    return show_status(request)


def login_view(request):
    chat_user = get_current_chat_user(request)
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login_chat_user(request, form.cleaned_data["user"])
        messages.success(request, "Welcome back to CialloChat.")
        return redirect("moments:status")
    return render(request, "moments/login.html", {"form": form, "chat_user": chat_user})


def register_view(request):
    chat_user = get_current_chat_user(request)
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        new_user = form.save()
        login_chat_user(request, new_user)
        messages.success(request, "Your CialloChat account is ready.")
        return redirect("moments:status")
    return render(
        request,
        "moments/register.html",
        {"form": form, "chat_user": chat_user, "avatars": AVATAR_CHOICES, "covers": BACKGROUND_CHOICES},
    )


def logout_view(request):
    logout_chat_user(request)
    messages.info(request, "CialloChat account signed out.")
    return redirect("moments:login")


def show_user(request):
    chat_user = get_current_chat_user(request)
    form = ProfileForm(request.POST or None, instance=chat_user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated.")
        return redirect("moments:user")
    statuses = Status.objects.filter(chat_user=chat_user).prefetch_related("likes", "comments")
    return render(
        request,
        "moments/user.html",
        {
            "chat_user": chat_user,
            "form": form,
            "statuses": statuses,
            "avatars": AVATAR_CHOICES,
            "covers": BACKGROUND_CHOICES,
        },
    )


def show_status(request):
    chat_user = get_current_chat_user(request)
    comments = Comment.objects.select_related("user", "parent", "parent__user")
    statuses = (
        Status.objects.select_related("chat_user", "user")
        .prefetch_related("likes", "likes__user", Prefetch("comments", queryset=comments))
        .all()
    )
    liked_status_ids = set(Like.objects.filter(user=chat_user).values_list("status_id", flat=True))
    return render(
        request,
        "moments/status.html",
        {
            "chat_user": chat_user,
            "statuses": statuses,
            "liked_status_ids": liked_status_ids,
            "comment_form": CommentForm(),
        },
    )


def submit_post(request):
    chat_user = get_current_chat_user(request)
    form = StatusForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        status = form.save(commit=False)
        status.chat_user = chat_user
        status.save()
        messages.success(request, "Moment published.")
        return redirect("moments:status")
    return render(request, "moments/my_post.html", {"chat_user": chat_user, "form": form})


def toggle_like(request, status_id):
    if request.method != "POST":
        return redirect("moments:status")
    chat_user = get_current_chat_user(request)
    status = get_object_or_404(Status, id=status_id)
    like = Like.objects.filter(status=status, user=chat_user).first()
    if like:
        like.delete()
    else:
        Like.objects.create(status=status, user=chat_user)
    return redirect("moments:status")


def add_comment(request, status_id):
    if request.method != "POST":
        return redirect("moments:status")
    chat_user = get_current_chat_user(request)
    status = get_object_or_404(Status, id=status_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.status = status
        comment.user = chat_user
        parent_id = request.POST.get("parent_id")
        if parent_id:
            comment.parent = get_object_or_404(Comment, id=parent_id, status=status)
        comment.save()
        messages.success(request, "Reply added." if comment.parent_id else "Comment added.")
    else:
        messages.error(request, "Comment cannot be empty.")
    return redirect("moments:status")


def delete_status(request, status_id):
    if request.method != "POST":
        return redirect("moments:status")
    chat_user = get_current_chat_user(request)
    status = get_object_or_404(Status, id=status_id)
    if not _can_manage_status(chat_user, status):
        return HttpResponseForbidden("You can only delete your own moments.")
    status.delete()
    messages.success(request, "Moment deleted.")
    return redirect("moments:status")


def delete_comment(request, comment_id):
    if request.method != "POST":
        return redirect("moments:status")
    chat_user = get_current_chat_user(request)
    comment = get_object_or_404(Comment.objects.select_related("status"), id=comment_id)
    if not (chat_user.is_admin or comment.user_id == chat_user.id or comment.status.chat_user_id == chat_user.id):
        return HttpResponseForbidden("You cannot delete this comment.")
    comment.delete()
    messages.success(request, "Comment deleted.")
    return redirect("moments:status")


def admin_panel(request):
    chat_user = get_current_chat_user(request)
    if not chat_user.is_admin:
        return HttpResponseForbidden("Admin account required.")
    statuses = Status.objects.select_related("chat_user").prefetch_related("comments", "likes")
    comments = Comment.objects.select_related("status", "user")[:50]
    return render(
        request,
        "moments/admin_panel.html",
        {"chat_user": chat_user, "statuses": statuses, "comments": comments},
    )


def _can_manage_status(chat_user, status):
    return chat_user.is_admin or status.chat_user_id == chat_user.id
