from django.db import models


class NewsModel(models.Model):
    id = models.CharField(max_length=20, primary_key = True)
    title = models.CharField(max_length = 60)
    author = models.CharField(max_length=20)
    url = models.CharField(max_length = 60)
    comments = models.CharField(max_length = 20)
    points = models.CharField(max_length = 20)
    label = models.CharField(max_length = 20)
