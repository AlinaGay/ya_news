import pytest
from django.conf import settings
from django.urls import reverse


@pytest.mark.django_db
def test_news_count(client, news_data):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, news_data):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, id_for_news):
    url = reverse('news:detail', args=id_for_news)
    response = client.get(url)
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


def test_anonymous_client_no_form(client, id_for_news):
    url = reverse('news:detail', args=id_for_news)
    response = client.get(url)
    assert 'form' not in response.context
    
