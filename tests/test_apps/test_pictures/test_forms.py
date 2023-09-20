import pytest

from server.apps.identity.models import User
from server.apps.pictures.intrastructure.django.forms import FavouritesForm


@pytest.mark.django_db()
def test_favourites_form(created_new_user: User) -> None:
    """Test favourites pictures form save method."""
    FavouritesForm(user=created_new_user).save(False)
