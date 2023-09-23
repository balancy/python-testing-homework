import os

import pytest

from server.apps.identity.infrastructure.services.placeholder import LeadCreate
from server.apps.identity.models import User
from server.settings.components.placeholder import PLACEHOLDER_API_URL


@pytest.mark.slow()
@pytest.mark.timeout(10)
@pytest.mark.parametrize(
    'url',
    [
        PLACEHOLDER_API_URL,
        pytest.param(
            'http://fakeapi:3000',
            marks=pytest.mark.skipif(
                os.getenv('DJANGO_ENV') == 'production',
                reason='This test is not supposed to be run in production',
            ),
        ),
    ],
)
@pytest.mark.django_db()
def test_lead_create_using_real_api(
    user_with_birthdate: User,
    url: str,
) -> None:
    """Tests LeadCreate for user on real API and local json-server."""
    LeadCreate(url, 10)(user=user_with_birthdate)
