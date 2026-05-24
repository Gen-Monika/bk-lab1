from django.urls import path

from . import views

app_name = "moments"

urlpatterns = [
    path("", views.home, name="home"),
    path("user/", views.show_user, name="user"),
    path("status/", views.show_status, name="status"),
    path("post/", views.submit_post, name="post"),
]
