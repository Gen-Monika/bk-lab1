import base64
import mimetypes
import os

from django import forms
from django.contrib.auth.hashers import check_password, make_password

from .assets import (
    ALLOWED_UPLOAD_EXTENSIONS,
    AVATAR_CHOICES,
    BACKGROUND_CHOICES,
    MAX_UPLOAD_SIZE,
    POST_IMAGE_CHOICES,
)
from .models import ChatUser, Comment, Status


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(min_length=6, widget=forms.PasswordInput)
    nickname = forms.CharField(max_length=40)
    avatar = forms.ChoiceField(choices=AVATAR_CHOICES)
    cover = forms.ChoiceField(choices=BACKGROUND_CHOICES)
    bio = forms.CharField(max_length=160, required=False)

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if not username.replace("_", "").replace("-", "").isalnum():
            raise forms.ValidationError("Username may only contain letters, numbers, hyphen and underscore.")
        if ChatUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already registered.")
        return username

    def save(self):
        return ChatUser.objects.create(
            username=self.cleaned_data["username"],
            password_hash=make_password(self.cleaned_data["password"]),
            nickname=self.cleaned_data["nickname"].strip(),
            avatar=self.cleaned_data["avatar"],
            cover=self.cleaned_data["cover"],
            bio=self.cleaned_data["bio"].strip(),
        )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if not username or not password:
            return cleaned_data
        user = ChatUser.objects.filter(username=username).first()
        if user is None or not check_password(password, user.password_hash):
            raise forms.ValidationError("Invalid username or password.")
        cleaned_data["user"] = user
        return cleaned_data


class ProfileForm(forms.ModelForm):
    avatar = forms.ChoiceField(choices=AVATAR_CHOICES)
    cover = forms.ChoiceField(choices=BACKGROUND_CHOICES)

    class Meta:
        model = ChatUser
        fields = ("nickname", "avatar", "cover", "bio")


class StatusForm(forms.ModelForm):
    pics = forms.ChoiceField(choices=POST_IMAGE_CHOICES, required=False)
    uploaded_image = forms.FileField(required=False)

    class Meta:
        model = Status
        fields = ("text", "pics", "uploaded_image")

    def clean_text(self):
        text = self.cleaned_data["text"].strip()
        if not text:
            raise forms.ValidationError("Say something before posting.")
        return text

    def clean_uploaded_image(self):
        uploaded = self.cleaned_data.get("uploaded_image")
        if not uploaded:
            return uploaded
        ext = os.path.splitext(uploaded.name)[1].lower()
        if ext not in ALLOWED_UPLOAD_EXTENSIONS:
            raise forms.ValidationError("Only jpg, png, webp and gif images are supported.")
        if uploaded.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError("Image size must be 3MB or smaller.")
        return uploaded

    def save(self, commit=True):
        status = super().save(commit=False)
        uploaded = self.cleaned_data.get("uploaded_image")
        if uploaded:
            content_type = mimetypes.guess_type(uploaded.name)[0] or getattr(uploaded, "content_type", "")
            content_type = content_type or "application/octet-stream"
            payload = base64.b64encode(uploaded.read()).decode("ascii")
            status.uploaded_image_data_url = f"data:{content_type};base64,{payload}"
            status.uploaded_image = None
        if commit:
            status.save()
            self.save_m2m()
        return status


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)

    def clean_text(self):
        text = self.cleaned_data["text"].strip()
        if not text:
            raise forms.ValidationError("Comment cannot be empty.")
        return text
