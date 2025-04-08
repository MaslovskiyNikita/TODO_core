import requests  # type: ignore[import-untyped]
from core.settings import AUTH_HOST, EMAIL_HOST_USER


class UserManagementClient:
    def get_users_email(self, user_ids):
        """

        auth_link = AUTH_HOST + "api/users/search"

        response = requests.post(
            auth_link,
            json={"user_ids": user_ids},
        )

        users = [user["email"] for user in response.json()["users"]]
        """
        return [EMAIL_HOST_USER]  # users


user_managment_client = UserManagementClient()
