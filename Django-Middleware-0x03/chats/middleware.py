# middleware.py
import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden


# -------------------- LOGGER CONFIGURATION --------------------
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


# -------------------- 1. REQUEST LOGGING MIDDLEWARE --------------------
class RequestLoggingMiddleware:
    """
    Logs each user's request to 'requests.log' including timestamp, user, and path.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'AnonymousUser'
        log_message = f"User: {user} - Path: {request.path}"
        logger.info(log_message)
        response = self.get_response(request)
        return response


# -------------------- 2. TIME-BASED ACCESS RESTRICTION --------------------
class RestrictAccessByTimeMiddleware:
    """
    Restricts access to the messaging app between 6 PM and 9 PM only.
    Outside this window, access returns a 403 Forbidden error.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if current_hour < 18 or current_hour >= 21:
            logger.warning(f"Access blocked due to time restriction. Path: {request.path}")
            return HttpResponseForbidden(
                "<h1>403 Forbidden</h1><p>Access restricted outside 6 PM–9 PM.</p>"
            )
        return self.get_response(request)


# -------------------- 3. RATE LIMIT MIDDLEWARE --------------------
class OffensiveLanguageMiddleware:
    """
    Limits the number of POST (message) requests per IP to 5 per minute.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_message_log = {}

    def __call__(self, request):
        if request.method == 'POST' and '/messages' in request.path:
            ip_address = self._get_client_ip(request)
            now = datetime.now()

            if ip_address not in self.ip_message_log:
                self.ip_message_log[ip_address] = []

            one_minute_ago = now - timedelta(minutes=1)
            self.ip_message_log[ip_address] = [
                ts for ts in self.ip_message_log[ip_address] if ts > one_minute_ago
            ]

            if len(self.ip_message_log[ip_address]) >= 5:
                logger.warning(f"Rate limit exceeded for IP: {ip_address}")
                return HttpResponseForbidden(
                    "<h1>403 Forbidden</h1><p>Message limit exceeded. Try again in one minute.</p>"
                )

            self.ip_message_log[ip_address].append(now)
            logger.info(f"Message sent by IP: {ip_address} at {now}")

        return self.get_response(request)

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


# -------------------- 4. ROLE-BASED PERMISSION MIDDLEWARE --------------------
class RolepermissionMiddleware:
    """
    Allows only users with roles 'admin' or 'moderator' to access restricted paths.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        restricted_paths = ['/admin-actions/', '/moderate/', '/manage/']

        if any(request.path.startswith(path) for path in restricted_paths):
            user = request.user
            if not user.is_authenticated:
                logger.warning("Unauthorized access attempt to restricted path.")
                return HttpResponseForbidden(
                    "<h1>403 Forbidden</h1><p>Authentication required.</p>"
                )

            user_role = getattr(user, 'role', None)
            if user_role not in ['admin', 'moderator']:
                logger.warning(f"Access denied for user {user} with role '{user_role}'")
                return HttpResponseForbidden(
                    "<h1>403 Forbidden</h1><p>You do not have permission to perform this action.</p>"
                )

            logger.info(f"Access granted for user {user} (role: {user_role})")

        return self.get_response(request)
