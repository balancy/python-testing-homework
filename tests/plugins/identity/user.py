from dataclasses import asdict, dataclass
from datetime import date
from typing import Protocol, TypeAlias

import pytest
from django.test import Client
from mimesis.schema import Field

from server.apps.identity.models import User

OptionalFields: TypeAlias = dict[str, str] | None


@dataclass(slots=True)
class UserData:
    """Model for user essential data model."""

    email: str
    first_name: str
    last_name: str
    job_title: str
    address: str
    phone: str


@dataclass(slots=True)
class RegistrationData(UserData):
    """Model for user essential data with passwords for registration."""

    password1: str
    password2: str


@dataclass(slots=True)
class UserDataWithDateOfBirth(UserData):
    """Model for user essential data with date of birth."""

    date_of_birth: date


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
) -> dict[str, str]:
    """Returns registration data with fake data."""
    return asdict(registration_data_factory())


@pytest.fixture()
def registration_data_with_empty_email(
    registration_data_factory: RegistrationDataFactory,
) -> dict[str, str]:
    """Returns registration data with fake data, but with empty email."""
    return asdict(registration_data_factory(email=''))  # type: ignore[call-arg]


@pytest.fixture()
def user_data(registration_data: dict[str, str]) -> UserData:
    """Simplified registration data with passwords dropped out."""
    registration_data_without_passwords = {
        field_name: field_value
        for field_name, field_value in registration_data.items()
        if not field_name.startswith('pass')
    }

    return UserData(**registration_data_without_passwords)


@pytest.fixture()
def user_data_with_birthdate(
    user_data: UserData,
    fake: Field,
) -> UserDataWithDateOfBirth:
    """Returns user data with date of birth."""
    return UserDataWithDateOfBirth(
        **{
            **asdict(user_data),
            'date_of_birth': fake('date'),
        },
    )


@pytest.fixture()
def random_password(fake: Field) -> str:
    """Returns random password."""
    return fake('password')


@pytest.mark.django_db()
@pytest.fixture()
def created_new_user(user_data: UserData) -> User:
    """Creates a new user in the database."""
    return User.objects.create(**asdict(user_data))


@pytest.mark.django_db()
@pytest.fixture()
def client_with_logged_in_user(
    created_new_user: User,
    client: Client,
) -> Client:
    """Returns logged in user."""
    client.force_login(created_new_user)
    return client
