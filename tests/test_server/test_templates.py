import pytest
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.test import RequestFactory
from django.urls import reverse

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture()
def index_request() -> WSGIRequest:
    """Returns request to index page."""
    return RequestFactory().get(reverse('index'))


def test_base_template(index_request: WSGIRequest) -> None:
    """Tests base template."""
    template_name: str = 'common/_base.html'

    page: HttpResponse = render(index_request, template_name)

    assert isinstance(page, HttpResponse)


@pytest.mark.timeout(3)
def test_messages_template(index_request: WSGIRequest) -> None:
    """Tests messages template."""
    template_name: str = 'common/includes/messages.html'

    page = render(
        index_request,
        template_name,
        {
            'messages': ['message'],
        },
    )

    assert isinstance(page, HttpResponse)
