import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User
from server.apps.pictures.logic.usecases.favourites_list import FavouritesList
from server.apps.pictures.models import FavouritePicture


@pytest.mark.django_db()
def test_fetch_favourite_picture_if_exists(
    created_new_user: User,
    created_fav_picture: FavouritePicture,
) -> None:
    """Test getting correct favourite pictures."""
    favourite_pictures = FavouritesList()
    user_fav_pictures = favourite_pictures(user_id=created_new_user.id)

    assert len(user_fav_pictures) == 1
    assert created_fav_picture in user_fav_pictures


@pytest.mark.django_db()
def test_logged_in_user_access_dashboard(
    created_new_user: User,
    client: Client,
) -> None:
    """Test that logged in user can access all views."""
    client.force_login(created_new_user)

    response = client.get(reverse('pictures:dashboard'))
    assert 'Профиль'.encode() in response.content


@pytest.mark.django_db()
def test_logged_in_user_access_favourite_pictures(
    created_new_user: User,
    client: Client,
    created_fav_picture: FavouritePicture,
) -> None:
    """Test that logged in user can access all views."""
    client.force_login(created_new_user)

    response = client.get(reverse('pictures:favourites'))
    assert 'Список любимых картинок'.encode() in response.content
    assert (
        'Номер {0}'.format(created_fav_picture.foreign_id).encode()
        in response.content
    )
