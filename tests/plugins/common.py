import pytest
from mimesis import Field, Locale


@pytest.fixture()
def fake() -> Field:
    """Returns mimesis field as basic element for generating data."""
    return Field(locale=Locale.RU)


@pytest.fixture()
def random_password(fake: Field) -> str:
    """Returns random password."""
    return fake('password')


@pytest.fixture()
def random_past_date(fake: Field) -> str:
    """Returns random date in the past."""
    return fake('date', start=1900, end=2000)
