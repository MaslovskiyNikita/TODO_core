import requests  # type: ignore[import-untyped]
from core.settings import EMAIL_HOST_USER


def get_users_email(user_ids):
    """
    response = requests.post(
        "http://auth-service/api/users/search",
        json={"user_ids": user_ids},
    )

    users = [user["email"] for user in response.json()["users"]]
    """
    return [EMAIL_HOST_USER]  # users
