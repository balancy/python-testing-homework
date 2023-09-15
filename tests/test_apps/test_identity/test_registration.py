from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User

if TYPE_CHECKING:
    from plugins.identity.user import (
        RegistrationData,
        RegistrationDataFactory,
        UserAssertion,
        UserData,
    )


@pytest.mark.django_db()
def test_valid_registration(
    client: Client,
    registration_data: 'RegistrationData',
    user_data: 'UserData',
    assert_correct_user: 'UserAssertion',
) -> None:
    """Tests that registration works with correct user data."""
    response = client.post(
        reverse('identity:registration'),
        data=registration_data.as_dict(),
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('identity:login')
    assert_correct_user(
        registration_data.email,
        user_data,
    )


@pytest.mark.django_db()
def test_registration_missing_email_field(
    client: Client,
    registration_data_factory: 'RegistrationDataFactory',
) -> None:
    """Tests that registration works with correct user data."""
    post_data = registration_data_factory(email='').as_dict()

    response = client.post(
        reverse('identity:registration'),
        data=post_data,
    )

    assert response.status_code == HTTPStatus.OK
    assert not User.objects.filter(email=post_data['email'])
