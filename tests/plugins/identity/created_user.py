from copy import copy
from datetime import date

import pytest
from django.test import Client
from plugins.custom_types import UserData

from server.apps.identity.models import User

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture()
def created_new_user(user_data: UserData) -> User:
    """Creates a new user in the database."""
    return User.objects.create(**user_data)


@pytest.fixture()
def client_logged_in(created_new_user: User, client: Client) -> Client:
    """Returns logged in user."""
    client.force_login(created_new_user)
    return client


@pytest.fixture()
def user_with_birthdate(
    created_new_user: User,
    random_past_date: date,
) -> User:
    """Returns user data with birthdate."""
    user_with_birthdate = copy(created_new_user)
    user_with_birthdate.date_of_birth = random_past_date

    return user_with_birthdate
