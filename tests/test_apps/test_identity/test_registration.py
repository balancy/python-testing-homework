from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User

pytestmark = [
    pytest.mark.django_db(),
]


@pytest.mark.parametrize(
    ('registration_data_fixture', 'status_code'),
    [
        ('registration_data', HTTPStatus.FOUND),
        ('registration_data_with_empty_email', HTTPStatus.OK),
    ],
)
def test_registration(
    client: Client,
    registration_data_fixture: str,
    status_code: int,
    request: pytest.FixtureRequest,
) -> None:
    """Tests if registration works correctly depending on user data."""
    registration_data = request.getfixturevalue(registration_data_fixture)

    response = client.post(
        reverse('identity:registration'),
        data=registration_data,
    )

    assert response.status_code == status_code


def test_registration_via_manager(random_password: str) -> None:
    """Tests if user manager allows register user without email."""
    with pytest.raises(ValueError, match='Users must have an email address'):
        User.objects.create_user(
            email='',
            password=random_password,
        )
