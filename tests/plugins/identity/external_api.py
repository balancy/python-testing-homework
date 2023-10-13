import json
from typing import Generator

import httpretty
import pytest
from mimesis import Field
from plugins.custom_types import ExternalApiUserResponse


@pytest.fixture()
def external_api_user_response(fake: Field) -> ExternalApiUserResponse:
    """Returns external api mock data for placeholder testing."""
    return ExternalApiUserResponse(id=fake('numeric.increment'))


@pytest.fixture()
def mocked_uri() -> str:
    """Returns mocked uri."""
    return 'https://example.com'


@pytest.fixture()
def external_api_mock(
    external_api_user_response: 'ExternalApiUserResponse',
    mocked_uri: str,
) -> Generator['ExternalApiUserResponse', None, None]:
    """Mock external api calls."""
    with httpretty.httprettized():
        httpretty.register_uri(
            method=httpretty.POST,
            body=json.dumps(external_api_user_response),
            uri='{0}/users'.format(mocked_uri),
        )
        yield external_api_user_response
        assert httpretty.has_request()
