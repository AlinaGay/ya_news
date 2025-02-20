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


def test_author_can_delete_comment(author_client, id_for_comment, id_for_news):
    url = reverse('news:delete', args=id_for_comment)
    response = author_client.delete(url)
    news_url = reverse('news:detail', args=id_for_news)
    url_to_comments = news_url + '#comments'
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_delete_comment_of_another_user(
        not_author_client,
        id_for_comment):
    url = reverse('news:delete', args=id_for_comment)
    response = not_author_client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(
        author_client,
        id_for_comment,
        comment_form_data,
        id_for_news,
        comment):
    news_url = reverse('news:detail', args=id_for_news)
    url_to_comments = news_url + '#comments'
    url = reverse('news:edit', args=id_for_comment)
    response = author_client.post(url, data=comment_form_data)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == comment_form_data['text']


def test_user_cant_edit_comment_of_another_user(
        not_author_client,
        id_for_comment,
        comment_form_data,
        comment):
    url = reverse('news:edit', args=id_for_comment)
    response = not_author_client.post(url, data=comment_form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text != comment_form_data['text']
