import os

import jwt
from core.DataClasses.UserDataClass import UserData
from django.http import JsonResponse
from dotenv import load_dotenv
from rest_framework.authentication import get_authorization_header

load_dotenv()


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = get_authorization_header(request).decode("utf-8")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                decoded_token = jwt.decode(
                    token, os.getenv("SECRET_KEY", "Nikita"), algorithms=["HS256"]
                )

                request.user_data = UserData(
                    name=decoded_token["name"],
                    uuid=decoded_token["uuid"],
                    role=decoded_token["role"],
                    permission=decoded_token["permission"],
                )

            except jwt.ExpiredSignatureError:
                return JsonResponse({"detail": "Token has expired."}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({"detail": "Invalid token."}, status=401)

        response = self.get_response(request)
        return response
