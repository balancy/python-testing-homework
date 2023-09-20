from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User
from server.apps.pictures.logic.usecases.favourites_list import FavouritesList
from server.apps.pictures.models import FavouritePicture

pytestmark = [
    pytest.mark.django_db(),
]


def test_fetch_favourite_picture_if_exists(
    created_new_user: User,
    created_fav_picture: FavouritePicture,
) -> None:
    """Tests getting correct favourite pictures."""
    user_fav_pictures = FavouritesList()(user_id=created_new_user.id)

    assert len(user_fav_pictures) == 1
    assert created_fav_picture in user_fav_pictures


def test_logged_in_user_access_dashboard_view(
    client_with_logged_in_user: Client,
) -> None:
    """Tests that logged in user can access dashboard view."""
    response = client_with_logged_in_user.get(
        reverse('pictures:dashboard'),
    )

    assert response.status_code == HTTPStatus.OK
    assert response.content


def test_logged_in_user_access_favourites_view(
    client_with_logged_in_user: Client,
    created_fav_picture: FavouritePicture,
) -> None:
    """Tests that logged in user can access favourites view."""
    response = client_with_logged_in_user.get(
        reverse('pictures:favourites'),
    )

    assert str(created_fav_picture).startswith('<Picture')
    assert response.status_code == HTTPStatus.OK
    assert response.content


def test_user_redirects_after_posting_picture(
    client_with_logged_in_user: Client,
    picture_data: dict[str, int | str],
) -> None:
    """Tests user redirects to dashboard view afetr posting picture."""
    response = client_with_logged_in_user.post(
        reverse('pictures:dashboard'),
        data=picture_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.headers['location'] == reverse('pictures:dashboard')
