from dataclasses import dataclass

import jwt
from django.http import JsonResponse
from rest_framework.authentication import get_authorization_header


@dataclass
class UserData:
    sub: str
    name: str
    uuid: str
    role: str


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = get_authorization_header(request).decode("utf-8")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                decoded_token = jwt.decode(token, "Nikita", algorithms=["HS256"])

                request.data_user = UserData(
                    sub=decoded_token["sub"],
                    name=decoded_token["name"],
                    uuid=decoded_token["uuid"],
                    role=decoded_token["role"],
                )

            except jwt.ExpiredSignatureError:
                return JsonResponse({"detail": "Token has expired."}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({"detail": "Invalid token."}, status=401)

        response = self.get_response(request)
        return response
