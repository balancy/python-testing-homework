import pytest
from mimesis import Field
from plugins.custom_types import FavouritePictureData

from server.apps.identity.models import User
from server.apps.pictures.models import FavouritePicture


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
    picture_data: dict[str, int | str],
) -> FavouritePicture:
    """Returns new created favourite picture."""
    return FavouritePicture.objects.create(
        user=created_new_user,
        **picture_data,
    )
