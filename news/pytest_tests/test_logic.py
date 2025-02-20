from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from news.forms import BAD_WORDS, WARNING
from news.models import Comment, News


def test_anonymous_user_cant_create_comment(
        client,
        id_for_news,
        comment_form_data):
    url = reverse('news:detail', args=id_for_news)
    client.post(url, data=comment_form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0
