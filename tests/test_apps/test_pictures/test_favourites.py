from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User
from server.apps.pictures.logic.usecases.favourites_list import FavouritesList
from server.apps.pictures.models import FavouritePicture

if TYPE_CHECKING:
    from plugins.custom_types import FavouritePictureData

pytestmark = [
    pytest.mark.django_db(),
]


def test_fetch_favourite_picture_if_exists(
    created_new_user: User,
    created_fav_picture: FavouritePicture,
) -> None:
    """Tests user gets correct favourite pictures via FavouritesList."""
    user_fav_pictures = FavouritesList()(user_id=created_new_user.id)

    assert len(user_fav_pictures) == 1
    assert created_fav_picture in user_fav_pictures


def test_logged_in_user_access_dashboard_view(
    client_logged_in: Client,
) -> None:
    """Tests logged in user can access dashboard view."""
    response = client_logged_in.get(
        reverse('pictures:dashboard'),
    )

    assert response.status_code == HTTPStatus.OK
    assert response.content


def test_logged_in_user_access_favourites_view(
    client_logged_in: Client,
    created_fav_picture: FavouritePicture,
) -> None:
    """Tests logged in user can access favourites view."""
    response = client_logged_in.get(
        reverse('pictures:favourites'),
    )

    assert str(created_fav_picture).startswith('<Picture')
    assert response.status_code == HTTPStatus.OK
    assert response.content


def test_user_redirects_after_posting_picture(
    client_logged_in: Client,
    picture_data: 'FavouritePictureData',
) -> None:
    """Tests user redirects to dashboard view after posting picture."""
    response = client_logged_in.post(
        reverse('pictures:dashboard'),
        data=picture_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.headers['location'] == reverse('pictures:dashboard')
