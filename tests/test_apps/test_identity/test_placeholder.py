from typing import TYPE_CHECKING

import httpretty

from server.apps.identity.intrastructure.services.placeholder import (
    LeadCreate,
    UserResponse,
)

if TYPE_CHECKING:
    from plugins.identity.user import UserDataWithDateOfBirth


@httpretty.activate(allow_net_connect=False, verbose=True)  # type: ignore[misc]
def test_lead_create_with_birthdate(
    user_data_with_birthdate: 'UserDataWithDateOfBirth',
) -> None:
    """Test LeadCreate object with birthday date."""
    uri = 'https://example.com'
    timeout = 5

    httpretty.register_uri(
        method=httpretty.POST,
        uri='{0}/users'.format(uri),
        body='{"id": 1}',
    )
    response = LeadCreate(uri, timeout)(user=user_data_with_birthdate)

    assert response == UserResponse(id=1)
