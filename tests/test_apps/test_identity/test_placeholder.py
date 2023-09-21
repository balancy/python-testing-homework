from typing import TYPE_CHECKING, Generator

import pytest

from server.apps.identity.infrastructure.services.placeholder import (
    LeadCreate,
    UserResponse,
)
from server.apps.identity.models import User

if TYPE_CHECKING:
    from plugins.identity.external_api import ExternalApiUserResponse


@pytest.mark.django_db()
def test_lead_create(
    user_with_birthdate: User,
    external_api_mock: Generator['ExternalApiUserResponse', None, None],
    mocked_uri: str,
) -> None:
    """Test LeadCreate object with birthday date."""
    response = LeadCreate(mocked_uri, 5)(user=user_with_birthdate)

    assert response == UserResponse(
        **external_api_mock,  # type: ignore[arg-type]
    )
