from random import SystemRandom

import pytest
from mimesis import Field, Locale


@pytest.fixture()
def faker_seed() -> int:
    """Returns seed for generating fake data."""
    cryptogen = SystemRandom()
    return cryptogen.randrange(100)


@pytest.fixture()
def fake(faker_seed: int) -> Field:
    """Returns mimesis field."""
    return Field(locale=Locale.RU, seed=faker_seed)


@pytest.fixture()
def random_password(fake: Field) -> str:
    """Returns random password."""
    return fake('password')
