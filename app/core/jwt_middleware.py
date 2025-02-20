import jwt
from django.conf import settings
from django.http import JsonResponse
from rest_framework.authentication import get_authorization_header


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = get_authorization_header(request).decode("utf-8")

        print(auth_header)
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                decoded_token = jwt.decode(token, "pizda", algorithms=["HS256"])

                request.data_user = {
                    "is_staff": True,
                }
            except jwt.ExpiredSignatureError:
                return JsonResponse({"detail": "Token has expired."}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({"detail": "Invalid token."}, status=401)

        response = self.get_response(request)
        return response
