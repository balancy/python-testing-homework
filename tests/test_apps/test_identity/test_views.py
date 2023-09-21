from http import HTTPStatus

import pytest
from django.urls import reverse

pytestmark = [
    pytest.mark.django_db(),
]


@pytest.mark.parametrize(
    ('client_fixture', 'view'),
    [
        ('client_logged_in', reverse('index')),
        ('client', reverse('identity:login')),
    ],
)
def test_views(
    client_fixture: str,
    view: str,
    request: pytest.FixtureRequest,
) -> None:
    """Test user see its views depending on auth status."""
    client = request.getfixturevalue(client_fixture)

    response = client.get(view)

    assert response.status_code == HTTPStatus.OK
