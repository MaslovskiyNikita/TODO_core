import requests  # type: ignore[import-untyped]
from core.settings import AUTH_HOST, EMAIL_HOST_USER


class UserManagementClient:
    def __init__(self):
        self.link = AUTH_HOST

    def get_users_email(self, user_ids: list[str]) -> list[str]:
        """

        auth_link = str(self.link) + "api/users/emails"

        response = requests.get(
            self.link,
            params={"user_ids": ",".join(user_ids)},
        )

        users_emails = response.json()["emails"]
        """
        return [EMAIL_HOST_USER]  # users
