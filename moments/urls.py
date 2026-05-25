from django.urls import path

from . import views

app_name = "moments"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("user/", views.show_user, name="user"),
    path("status/", views.show_status, name="status"),
    path("post/", views.submit_post, name="post"),
    path("status/<int:status_id>/like/", views.toggle_like, name="toggle_like"),
    path("status/<int:status_id>/comment/", views.add_comment, name="add_comment"),
    path("status/<int:status_id>/delete/", views.delete_status, name="delete_status"),
    path("comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),
    path("admin-panel/", views.admin_panel, name="admin_panel"),
]
