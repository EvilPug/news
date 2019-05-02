from django.db import models
from django.utils import timezone


class NewsModel(models.Model):
    id = models.AutoField(max_length=5, primary_key = True)
    title = models.CharField(max_length = 80)
    author = models.CharField(max_length=15)
    url = models.CharField(max_length = 400)
    comments = models.CharField(max_length = 5)
    points = models.CharField(max_length = 5)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def was_added_recently(self):
        now = timezone.now()
        return now - timezone.timedelta(days=1) <= self.added_date <= now
