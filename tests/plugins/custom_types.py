from datetime import date
from typing import Protocol, TypedDict, final


@final
class UserData(TypedDict, total=False):
    """Model for user essential data model."""

    email: str
    first_name: str
    last_name: str
    job_title: str
    address: str
    phone: str
    date_of_birth: date


@final
class RegistrationData(TypedDict, total=False):
    """Model for user essential data with passwords for registration."""

    password1: str
    password2: str


class RegistrationDataFactory(Protocol):
    """Registration data factory protocol."""

    def __call__(self) -> RegistrationData:
        """Factory must implement being called."""
        ...


@final
class ExternalApiUserResponse(TypedDict):
    """Model for external API data."""

    id: int


@final
class FavouritePictureData(TypedDict, total=False):
    """Model for essential favourite picture data."""

    foreign_id: int
    url: str
