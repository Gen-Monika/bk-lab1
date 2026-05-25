from django.contrib.auth.hashers import check_password
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from blueapps.account.models import User
from moments import views

from moments.forms import RegisterForm, StatusForm
from moments.models import ChatUser, Comment, Like, Status
from moments.services import ensure_default_admin


class CialloChatModelTests(TestCase):
    def test_default_admin_is_created_once(self):
        admin = ensure_default_admin()
        second = ensure_default_admin()
        self.assertEqual(admin.id, second.id)
        self.assertTrue(admin.is_admin)
        self.assertTrue(check_password("admin123456", admin.password_hash))

    def test_like_is_unique_per_user_and_status(self):
        user = ChatUser.objects.create(
            username="alice",
            password_hash="hash",
            nickname="Alice",
        )
        status = Status.objects.create(chat_user=user, text="Ciallo")
        Like.objects.create(user=user, status=status)
        with self.assertRaises(Exception):
            Like.objects.create(user=user, status=status)


class CialloChatFormTests(TestCase):
    def test_register_rejects_duplicate_username(self):
        ChatUser.objects.create(username="alice", password_hash="hash", nickname="Alice")
        form = RegisterForm(
            {
                "username": "alice",
                "password": "secret123",
                "nickname": "Alice 2",
                "avatar": "ciallo/characters/murasame.png",
                "cover": "ciallo/bg/clubroom.png",
                "bio": "",
            }
        )
        self.assertFalse(form.is_valid())

    def test_status_text_must_not_be_empty(self):
        form = StatusForm({"text": "", "pics": ""})
        self.assertFalse(form.is_valid())

    def test_status_accepts_image_upload(self):
        upload = SimpleUploadedFile("moment.png", b"image-bytes", content_type="image/png")
        form = StatusForm({"text": "With image", "pics": ""}, {"uploaded_image": upload})
        self.assertTrue(form.is_valid())


class CialloChatViewTests(TestCase):
    def setUp(self):
        for view in (
            views.show_status,
            views.submit_post,
            views.toggle_like,
            views.add_comment,
        ):
            view.login_exempt = True
        self.client = Client()
        self.blueking_user = User.objects.create_user(username="bk_alice", password="unused")
        self.client.force_login(self.blueking_user)
        self.user = ChatUser.objects.create(
            username="alice",
            password_hash="hash",
            nickname="Alice",
            avatar="ciallo/characters/noa.png",
            cover="ciallo/bg/sky.png",
        )
        session = self.client.session
        session["ciallo_chat_user_id"] = self.user.id
        session.save()

    def test_feed_page_renders(self):
        response = self.client.get(reverse("moments:status"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CialloChat")

    def test_post_like_and_comment_flow(self):
        response = self.client.post(reverse("moments:post"), {"text": "Hello", "pics": ""})
        self.assertEqual(response.status_code, 302)
        status = Status.objects.get(text="Hello")

        response = self.client.post(reverse("moments:toggle_like", args=[status.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Like.objects.filter(status=status, user=self.user).exists())

        response = self.client.post(reverse("moments:add_comment", args=[status.id]), {"text": "Nice"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(status=status, user=self.user, text="Nice").exists())

    def test_post_with_uploaded_image(self):
        upload = SimpleUploadedFile("moment.png", b"image-bytes", content_type="image/png")
        response = self.client.post(
            reverse("moments:post"),
            {"text": "Uploaded", "pics": "", "uploaded_image": upload},
        )
        self.assertEqual(response.status_code, 302)
        status = Status.objects.get(text="Uploaded")
        self.assertTrue(status.uploaded_image.name.startswith("ciallo_uploads/"))
