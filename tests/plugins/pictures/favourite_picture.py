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

    def as_dict(self) -> dict[str, str | int]:
        """Return as a dictionary."""
        return asdict(self)


@pytest.fixture()
def picture_data(fake: Field) -> FavouritePictureData:
    """Returns favourite picture data."""
    return FavouritePictureData(
        foreign_id=fake('numeric.increment'),
        url=fake('internet.uri'),
    )


@pytest.mark.django_db()
@pytest.fixture()
def created_fav_picture(
    created_new_user: User,
    picture_data: 'FavouritePictureData',
) -> FavouritePicture:
    """Create new favourite picture."""
    created_picture = FavouritePicture.objects.create(
        user=created_new_user,
        **picture_data.as_dict(),
    )
    assert str(created_picture).startswith(
        '<Picture {0}'.format(picture_data.foreign_id),
    )
    return created_picture
