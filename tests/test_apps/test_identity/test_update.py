from http import HTTPStatus

import pytest
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture()
def get_update_view(client_with_logged_in_user: Client) -> HttpResponse:
    """Gets response from user update view."""
    return client_with_logged_in_user.get(  # type: ignore[return-value]
        reverse('identity:user_update'),
    )


@pytest.fixture()
def post_update_view(
    client_with_logged_in_user: Client,
    registration_data: dict[str, str],
) -> HttpResponse:
    """Posts data for update to update view."""
    return client_with_logged_in_user.post(  # type: ignore[return-value]
        reverse('identity:user_update'),
        data=registration_data,
    )


@pytest.mark.parametrize(
    ('request_fixture', 'status_code'),
    [
        ('get_update_view', HTTPStatus.OK),
        ('post_update_view', HTTPStatus.FOUND),
    ],
)
def test_update(
    request_fixture: str,
    status_code: int,
    request: pytest.FixtureRequest,
) -> None:
    """Tests if update view works correctly depending on request method."""
    response = request.getfixturevalue(request_fixture)

    assert response.status_code == status_code
