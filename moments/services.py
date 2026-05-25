from django.conf import settings
from django.contrib.auth.hashers import make_password

from .models import ChatUser


SESSION_KEY = "ciallo_chat_user_id"
ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123456"


def get_current_chat_user(request):
    user_id = request.session.get(SESSION_KEY)
    if not user_id:
        return ensure_default_admin()
    user = ChatUser.objects.filter(id=user_id).first()
    if user is None:
        user = ensure_default_admin()
        request.session[SESSION_KEY] = user.id
    return user


def login_chat_user(request, user):
    request.session[SESSION_KEY] = user.id


def logout_chat_user(request):
    request.session.pop(SESSION_KEY, None)


def ensure_default_admin():
    password = getattr(settings, "CIALLO_ADMIN_PASSWORD", DEFAULT_ADMIN_PASSWORD)
    admin, created = ChatUser.objects.get_or_create(
        username=ADMIN_USERNAME,
        defaults={
            "password_hash": make_password(password),
            "nickname": "Ciallo Admin",
            "avatar": "ciallo/characters/murasame.png",
            "cover": "ciallo/bg/clubroom.png",
            "bio": "Default administrator for course demonstration.",
            "is_admin": True,
        },
    )
    if not admin.is_admin:
        admin.is_admin = True
        admin.save(update_fields=["is_admin"])
    return admin
