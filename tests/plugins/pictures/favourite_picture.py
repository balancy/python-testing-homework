from dataclasses import asdict, dataclass

import pytest
from mimesis import Field

from server.apps.identity.models import User
from server.apps.pictures.models import FavouritePicture


@dataclass(slots=True)
class FavouritePictureData:
    """Essential favourite picture data model."""

    foreign_id: int
    url: str

    def asdict(self) -> dict[str, int | str]:
        """Return favourite picture data as dict."""
        return asdict(self)


@pytest.fixture()
def picture_data(fake: Field) -> dict[str, int | str]:
    """Returns favourite picture data."""
    return FavouritePictureData(
        foreign_id=fake('numeric.increment'),
        url=fake('internet.uri'),
    ).asdict()


@pytest.mark.django_db()
@pytest.fixture()
def created_fav_picture(
    created_new_user: User,
    picture_data: dict[str, int | str],
) -> FavouritePicture:
    """Returns new created favourite picture."""
    return FavouritePicture.objects.create(
        user=created_new_user,
        **picture_data,
    )
