from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


from news.forms import BAD_WORDS, WARNING
from news.models import Comment, News


User = get_user_model()


class TestCommentCreation(TestCase):

    COMMENT_TEXT = 'Текст комментария'

    @classmethod
    def setUpTestData(cls):
        cls.news = News.objects.create(title='Заголовок', text='Текст')
        cls.url = reverse('news:detail', args=(cls.news.id,))
        cls.user = User.objects.create(username='Мимо Крокодил')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.form_data = {'text': cls.COMMENT_TEXT}
