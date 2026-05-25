import os

from django.contrib.auth.hashers import make_password
from django.db import migrations


def seed_admin(apps, schema_editor):
    ChatUser = apps.get_model("moments", "ChatUser")
    password = os.getenv("CIALLO_ADMIN_PASSWORD", "admin123456")
    admin, created = ChatUser.objects.get_or_create(
        username="admin",
        defaults={
            "password_hash": make_password(password),
            "nickname": "Ciallo Admin",
            "avatar": "ciallo/characters/murasame.png",
            "cover": "ciallo/bg/clubroom.png",
            "bio": "Default administrator for course demonstration.",
            "is_admin": True,
        },
    )
    if not created and not admin.is_admin:
        admin.is_admin = True
        admin.save(update_fields=["is_admin"])


class Migration(migrations.Migration):

    dependencies = [
        ("moments", "0002_auto_20260525_1307"),
    ]

    operations = [
        migrations.RunPython(seed_admin, migrations.RunPython.noop),
    ]
