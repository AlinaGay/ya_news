from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertFormError

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


def test_user_can_create_comment(
        author,
        author_client,
        id_for_news,
        comment_form_data):
    url = reverse('news:detail', args=id_for_news)
    response = author_client.post(url, data=comment_form_data)
    comments_count = Comment.objects.count()
    comment = Comment.objects.get()
    news_from_db = News.objects.get()

    assertRedirects(response, f'{url}#comments')
    assert comments_count == 1
    assert comment.text == comment_form_data['text']
    assert comment.news == news_from_db
    assert comment.author == author

def test_user_cant_use_bad_words(author_client, id_for_news, bad_words_data):
    url = reverse('news:detail', args=id_for_news)
    response = author_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0
