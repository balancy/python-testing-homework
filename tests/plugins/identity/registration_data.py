import pytest
from mimesis.schema import Field
from plugins.custom_types import (
    RegistrationData,
    RegistrationDataFactory,
    UserData,
)


@pytest.fixture()
def registration_data_factory(fake: Field) -> RegistrationDataFactory:
    """Returns registration data with fake data."""

    def factory(**fields: RegistrationData) -> RegistrationData:
        """Return factory for fake registration data."""
        password = fake('password')

        return RegistrationData(
            email=fake('email'),
            first_name=fake('first_name'),
            last_name=fake('last_name'),
            job_title=fake('occupation'),
            address=fake('city'),
            phone=fake('telephone'),
            password1=password,
            password2=password,
            **fields,
        )

    return factory


@pytest.fixture()
def registration_data(
    registration_data_factory: RegistrationDataFactory,
) -> RegistrationData:
    """Returns instance of registration data factory."""
    return registration_data_factory()


@pytest.fixture()
def user_data(registration_data: RegistrationData) -> UserData:
    """Returns registration data with passwords dropped out."""
    return {
        field_name: field_value
        for field_name, field_value in registration_data.items()
        if not field_name.startswith('pass')
    }


@pytest.fixture()
def registration_data_with_empty_email(
    registration_data_factory: RegistrationDataFactory,
) -> RegistrationData:
    """Returns registration data, but with empty email."""
    reg_data = registration_data_factory()
    reg_data['email'] = ''
    return reg_data
