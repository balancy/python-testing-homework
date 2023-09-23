from typing import TYPE_CHECKING, Generator

import pytest

from server.apps.identity.infrastructure.services.placeholder import (
    LeadCreate,
    UserResponse,
)
from server.apps.identity.models import User
from server.settings.components.placeholder import PLACEHOLDER_API_URL

if TYPE_CHECKING:
    from plugins.identity.external_api import ExternalApiUserResponse


pytestmark = [
    pytest.mark.django_db(),
]


def test_lead_create_using_mocked_api(
    user_with_birthdate: User,
    external_api_mock: Generator['ExternalApiUserResponse', None, None],
    mocked_uri: str,
) -> None:
    """Tests LeadCreate for user with birthday date on mocked API."""
    response = LeadCreate(mocked_uri, 5)(user=user_with_birthdate)

    assert response == UserResponse(
        **external_api_mock,  # type: ignore[arg-type]
    )


@pytest.mark.slow()
@pytest.mark.timeout(10)
@pytest.mark.parametrize('url', [PLACEHOLDER_API_URL, 'http://fakeapi:3000'])
def test_lead_create_using_real_api(
    user_with_birthdate: User,
    url: str,
) -> None:
    """Tests LeadCreate for user on real API and local json-server."""
    LeadCreate(url, 10)(user=user_with_birthdate)
