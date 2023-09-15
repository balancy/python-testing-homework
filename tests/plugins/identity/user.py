from random import randint
from typing import Callable, Protocol, TypeAlias, TypedDict, Unpack, final

import pytest
from mimesis.locales import Locale
from mimesis.schema import Field, Schema

from server.apps.identity.models import User


@pytest.fixture
def faker_seed() -> int:
    """Returns seed for generating fake data."""
    return randint(0, 1000)


class UserData(TypedDict, total=False):
    """Represents simplified data for user registration.

    Doesn't include password fields. Importing is allowed only under
    ``if TYPE_CHECKING`` in tests.
    """

    email: str
    first_name: str
    last_name: str
    job_title: str
    address: str
    phone_type: int


@final
class RegistrationData(UserData, total=False):
    """Represents all data necessary for user registration.

    Importing this type is only allowed uner ``if TYPE_CHECKING`` in tests.
    """

    password1: str
    password2: str


@final
class RegistrationDataFactory(Protocol):
    def __call__(self, **fields: Unpack[RegistrationData]) -> RegistrationData:
        """User data factory protocole."""
        ...


@pytest.fixture
def registration_data_factory(faker_seed: int) -> RegistrationDataFactory:
    """Returns factory for generating fake registration data."""

    def factory(**fields: Unpack[RegistrationData]) -> RegistrationData:
        fake = Field(locale=Locale.RU, seed=faker_seed)
        schema = Schema(
            lambda: {
                'email': fake('email'),
                'first_name': fake('first_name'),
                'last_name': fake('last_name'),
                'phone': fake('telephone'),
                'job_title': fake('occupation'),
                'address': fake('city'),
                'date_of_birth': fake('datetime.date'),
            },
            iterations=1,
        )
        fake_details, *_ = schema.create()
        password = fake('password')
        return {
            **fake_details,  # type: ignore[misc]
            **{'password1': password, 'password2': password},
            **fields,
        }

    return factory


@pytest.fixture
def user_data(registration_data: RegistrationData) -> UserData:
    """Simplified registration data with passwords dropped out."""

    return {  # type: ignore[return-value]
        key: value
        for key, value in registration_data.items()
        if not key.startswith('password')
    }


@pytest.fixture()
def registration_data(
    registration_data_factory: RegistrationDataFactory,
) -> RegistrationData:
    """Default success registration data."""
    return registration_data_factory()


UserAssertion: TypeAlias = Callable[[str, UserData], None]


@pytest.fixture(scope='session')
def assert_correct_user() -> UserAssertion:
    def factory(email: str, expected: UserData) -> None:
        user = User.objects.get(email=email)
        assert user.id  # type: ignore[unreachable]
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff

        for field_name, data_value in expected.items():
            assert getattr(user, field_name) == data_value

    return factory
