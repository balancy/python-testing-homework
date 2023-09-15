from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User


@pytest.mark.django_db()
def test_valid_login(
    client: Client,
    created_new_user: User,
) -> None:
    """Tests that login works with correct user data."""
    client.force_login(created_new_user)

    response = client.get(reverse('index'))
    assert 'Выход'.encode() in response.content


@pytest.mark.django_db()
def test_login_view_uses_login_template(client: Client) -> None:
    """Tests that login view uses correct template."""
    response = client.get(reverse('identity:login'))

    assert response.status_code == HTTPStatus.OK
    assert 'Войти в личный кабинет'.encode() in response.content
    assert 'Have fun!'.encode() in response.content
