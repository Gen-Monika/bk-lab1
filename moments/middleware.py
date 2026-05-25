from .models import UserActionLog
from .services import get_current_chat_user


class UserActionLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith("/static/") or request.path.startswith("/admin/jsi18n/"):
            return response
        chat_user = None
        try:
            chat_user = get_current_chat_user(request)
        except Exception:
            chat_user = None
        blueking_user = ""
        if getattr(request, "user", None) and request.user.is_authenticated:
            blueking_user = request.user.username
        UserActionLog.objects.create(
            blueking_user=blueking_user,
            chat_user=chat_user,
            method=request.method,
            path=request.path[:255],
            status_code=getattr(response, "status_code", None),
            ip_address=self._client_ip(request),
        )
        return response

    def _client_ip(self, request):
        forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
