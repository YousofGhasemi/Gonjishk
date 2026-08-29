from django.conf import settings
from rest_framework.response import Response


def set_auth_cookies(response: Response, access: str, refresh: str) -> None:
    jwt_settings = settings.SIMPLE_JWT

    response.set_cookie(
        key=jwt_settings["AUTH_COOKIE"],
        value=access,
        max_age=int(jwt_settings["ACCESS_TOKEN_LIFETIME"].total_seconds()),
        httponly=jwt_settings["AUTH_COOKIE_HTTP_ONLY"],
        secure=jwt_settings["AUTH_COOKIE_SECURE"],
        samesite=jwt_settings["AUTH_COOKIE_SAMESITE"],
    )
    response.set_cookie(
        key=jwt_settings["AUTH_COOKIE_REFRESH"],
        value=refresh,
        max_age=int(jwt_settings["REFRESH_TOKEN_LIFETIME"].total_seconds()),
        httponly=jwt_settings["AUTH_COOKIE_HTTP_ONLY"],
        secure=jwt_settings["AUTH_COOKIE_SECURE"],
        samesite=jwt_settings["AUTH_COOKIE_SAMESITE"],
    )


def clear_auth_cookies(response: Response) -> None:
    jwt_settings = settings.SIMPLE_JWT
    response.delete_cookie(jwt_settings["AUTH_COOKIE"])
    response.delete_cookie(jwt_settings["AUTH_COOKIE_REFRESH"])
