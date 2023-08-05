"""Users API"""
from urllib.parse import quote

from open_discussions_api.base import BaseApi

SUPPORTED_USER_ATTRIBUTES = (
    'name',
    'image',
    'image_small',
    'image_medium',
)


class UsersApi(BaseApi):
    """Users API"""

    def list(self):
        """
        Returns a list of users

        Returns:
            requests.Response: A response containing the data for all users in open-discussions
        """
        return self.session.get(self.get_url("/users/"))

    def get(self, username):
        """
        Gets a specific user

        Args:
            username (str): The username for the user

        Returns:
            requests.Response: A response containing the user's data
        """
        return self.session.get(self.get_url("/users/{}/").format(quote(username)))

    def create(self, **profile):
        """
        Creates a new user

        Args:
            profile (dict): attributes used in creating the profile. See SUPPORTED_USER_ATTRIBUTES for a list.

        Returns:
            requests.Response: A response containing the newly created profile data
        """
        if not profile:
            raise AttributeError("No fields provided to create")

        for key in profile:
            if key not in SUPPORTED_USER_ATTRIBUTES:
                raise AttributeError("Argument {} is not supported".format(key))

        return self.session.post(
            self.get_url("/users/"),
            json=dict(profile=profile or {})
        )

    def update(self, username, **profile):
        """
        Gets a specific user

        Args:
            username (str): The username of the user
            profile (dict):
                Attributes of the profile to update for that user. See SUPPORTED_USER_ATTRIBUTES for a valid list.

        Returns:
            requests.Response: A response containing the updated user profile data
        """
        if not profile:
            raise AttributeError("No fields provided to update")

        for key in profile:
            if key not in SUPPORTED_USER_ATTRIBUTES:
                raise AttributeError("Argument {} is not supported".format(key))

        return self.session.patch(
            self.get_url("/users/{}/".format(quote(username))),
            json=dict(profile=profile)
        )
