"""Users API"""
import json

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
        """Returns a list of users"""
        return self.session.get(self.get_url("/users/"))

    def get(self, username):
        """Gets a specific user"""
        return self.session.get(self.get_url("/users/{}").format(username))

    def create(self, **profile):
        """Creates a new user"""
        if not profile:
            raise AttributeError("No fields provided to create")

        for key in profile:
            if key not in SUPPORTED_USER_ATTRIBUTES:
                raise AttributeError("Argument {} is not supported".format(key))

        return self.session.post(
            self.get_url("/users/"),
            data=json.dumps(dict(profile=profile or {}))
        )

    def update(self, username, **profile):
        """Gets a specific user"""
        if not profile:
            raise AttributeError("No fields provided to update")

        for key in profile:
            if key not in SUPPORTED_USER_ATTRIBUTES:
                raise AttributeError("Argument {} is not supported".format(key))

        return self.session.patch(
            self.get_url("/users/{}/".format(username)),
            data=json.dumps(dict(profile=profile))
        )
