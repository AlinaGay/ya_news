from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects

import pytest


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('news:detail', pytest.lazy_fixture('id_for_news')),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
    ),
)
def test_pages_availability_for_anonymous_user(not_author_client, name, args):
    url = reverse(name, args=args)
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('not_author_client'),HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', pytest.lazy_fixture('id_for_comment')),
        ('news:delete', pytest.lazy_fixture('id_for_comment')),
    ),
)
def test_availability_for_author_for_edit_and_delete_of_comment(
        parametrized_client, name, args, expected_status):
    url = reverse(name, args=args)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', pytest.lazy_fixture('id_for_comment')),
        ('news:delete', pytest.lazy_fixture('id_for_comment')),
    ),
)
def test_redirect_for_anonymous_client(client, name, args):
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
