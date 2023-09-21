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
    """Returns registration data with fake data."""
    return registration_data_factory()


@pytest.fixture()
def user_data(registration_data: RegistrationData) -> UserData:
    """Simplified registration data with passwords dropped out."""
    return {
        field_name: field_value
        for field_name, field_value in registration_data.items()
        if not field_name.startswith('pass')
    }


@pytest.fixture()
def registration_data_with_empty_email(
    registration_data: RegistrationData,
) -> RegistrationData:
    """Returns registration data with fake data, but with empty email."""
    reg_data_with_empty_email = registration_data.copy()
    reg_data_with_empty_email['email'] = ''
    return reg_data_with_empty_email
