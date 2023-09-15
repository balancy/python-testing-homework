from dataclasses import asdict, dataclass
from random import SystemRandom
from typing import Callable, TypeAlias

import pytest
from mimesis.locales import Locale
from mimesis.schema import Field

from server.apps.identity.models import User


@dataclass(frozen=True, slots=True)
class UserData:
    """Stores user essential data."""

    email: str
    first_name: str
    last_name: str
    job_title: str
    address: str
    phone: str


@dataclass(frozen=True, slots=True)
class RegistrationData(UserData):
    """Stores user essential data with passwords for registration."""

    password1: str
    password2: str

    def as_dict(self) -> dict[str, str]:
        """Represents registration data in a dictionary form."""
        return asdict(self)


@pytest.fixture()
def faker_seed() -> int:
    """Returns seed for generating fake data."""
    cryptogen = SystemRandom()
    return cryptogen.randrange(100)


@pytest.fixture()
def registration_data(faker_seed: int) -> RegistrationData:
    """Returns registration data with fake data."""
    fake = Field(locale=Locale.RU, seed=faker_seed)
    password = fake('password')
    return RegistrationData(
        email=fake('email'),
        first_name=fake('first_name'),
        last_name=fake('last_name'),
        phone=fake('telephone'),
        job_title=fake('occupation'),
        address=fake('city'),
        password1=password,
        password2=password,
    )


@pytest.fixture()
def user_data(registration_data: RegistrationData) -> UserData:
    """Simplified registration data with passwords dropped out."""
    registration_data_without_passwords = {
        field_name: field_value
        for field_name, field_value in asdict(registration_data).items()
        if not field_name.startswith('pass')
    }

    return UserData(**registration_data_without_passwords)


UserAssertion: TypeAlias = Callable[[str, UserData], None]


@pytest.fixture(scope='session')
def assert_correct_user() -> UserAssertion:
    """Asserts that user with given email exists and has expected data."""

    def factory(email: str, expected: UserData) -> None:
        user = User.objects.get(email=email)
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff

        for field_name, field_value in asdict(expected).items():
            assert getattr(user, field_name) == field_value

    return factory
