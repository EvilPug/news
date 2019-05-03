from django.test import TestCase
from django.utils import timezone
from news.models import NewsModel

class NewsModelTests(TestCase):

    def test_can_create_news(self):
        news = NewsModel.objects.create(title='News title',
                                   author='News author',
                                   url='News url',
                                   comments='News comments',
                                   points='News points')
        self.assertTrue(news)

    def test_string_representation(self):
        news = NewsModel.objects.create(title='News title',
                                   author='News author',
                                   url='News url',
                                   comments='News comments',
                                   points='News points')
        self.assertEqual(str(news), 'News title')


    def test_was_added_recently(self):
        time = timezone.now() + timezone.timedelta(days=30)
        future_news = NewsModel(added_date=time)
        self.assertEqual(future_news.was_added_recently(), False)
