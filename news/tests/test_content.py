from datetime import datetime, timedelta
from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from news.models import News


class TestHomePage(TestCase):

    HOME_URL = reverse('news:home')

    @classmethod
    def setUpTestData(cls):
        today = datetime.today()
        all_news = [
            News(
                title=f'Новость {index}',
                text='Просто текст.',
                date=today - timedelta(days=index)
            )
            for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
        ]
        News.objects.bulk_create(all_news)

    def test_news_count(self):
        response = self.client.get(self.HOME_URL)
        object_list = response.context['object_list']
        news_count = object_list.count()
        self.assertEqual(news_count, settings.NEWS_COUNT_ON_HOME_PAGE)
