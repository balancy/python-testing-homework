from dataclasses import asdict, dataclass
from typing import Callable, Protocol, TypeAlias

import pytest
from mimesis.schema import Field

from server.apps.identity.models import User

OptionalFields: TypeAlias = dict[str, str] | None


@dataclass(slots=True)
class UserData:
    """User essential data model."""

    email: str
    first_name: str
    last_name: str
    job_title: str
    address: str
    phone: str

    def as_dict(self) -> dict[str, str]:
        """Represents user data in a dictionary form."""
        return asdict(self)


@dataclass(slots=True)
class RegistrationData(UserData):
    """User essential data with passwords for registration model."""

    password1: str
    password2: str


class RegistrationDataFactory(Protocol):
    """Registration data factory protocol."""

    def __call__(self) -> RegistrationData:
        """Factory must implement being called."""
        ...


@pytest.fixture()
def registration_data_factory(fake: Field) -> RegistrationDataFactory:
    """Returns registration data with fake data."""

    def factory(**fields: OptionalFields) -> RegistrationData:
        password = fake('password')
        email = str(fields.get('email', fake('email')))

        return RegistrationData(
            email=email,
            first_name=fake('first_name'),
            last_name=fake('last_name'),
            phone=fake('telephone'),
            job_title=fake('occupation'),
            address=fake('city'),
            password1=password,
            password2=password,
        )

    return factory


@pytest.fixture()
def registration_data(
    registration_data_factory: RegistrationDataFactory,
) -> RegistrationData:
    """Returns registration data with fake data."""
    return registration_data_factory()


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

    def factory(
        email: str,
        expected: UserData,
    ) -> None:
        user = User.objects.get(email=email)
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff

        for field_name, field_value in asdict(expected).items():
            assert getattr(user, field_name) == field_value

    return factory


@pytest.mark.django_db()
@pytest.fixture()
def created_new_user(user_data: UserData) -> User:
    """Creates a new user in the database."""
    return User.objects.create(**asdict(user_data))
