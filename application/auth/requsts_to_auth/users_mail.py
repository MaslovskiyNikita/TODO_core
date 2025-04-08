import requests  # type: ignore[import-untyped]
from core.settings import AUTH_HOST, EMAIL_HOST_USER


class UserManagementClient:
    def __init__(self):
        self.link = AUTH_HOST + "api/users/emails"

    def get_users_email(self, user_ids: list[str]) -> list[str]:
        """

        response = requests.get(
            self.link,
            params={"user_ids": user_ids},
        )

        users_emails = response.json()["emails"]
        """
        return [EMAIL_HOST_USER]  # users
