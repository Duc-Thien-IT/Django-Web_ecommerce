from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class SessionTimeoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            # Kiểm tra xem có yêu cầu "remember me" không
            if not request.session.get('remember_me', False):
                # Nếu không có "remember me", thiết lập thời gian hết hạn phiên
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            else:
                # Nếu có "remember me", thiết lập thời gian hết hạn phiên dài hơn
                request.session.set_expiry(settings.SESSION_COOKIE_AGE * 4)  # 4 lần thời gian mặc định
        return None