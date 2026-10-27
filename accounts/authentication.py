from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed


class SafeJWTAuthentication(JWTAuthentication):
    """
    Safe JWT Authentication:
    If a valid JWT token is provided, authenticates the user.
    If an invalid, expired, or malformed token is provided, safely returns None
    (treating the user as AnonymousUser) rather than raising an unhandled AuthenticationFailed
    which breaks public read endpoints with 401 errors.
    Views requiring authentication will still enforce permissions via IsAuthenticated.
    """
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
            return self.get_user(validated_token), validated_token
        except (InvalidToken, AuthenticationFailed, Exception):
            # Fall back to anonymous access for public views
            return None
