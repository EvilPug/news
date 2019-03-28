from django.db import models


class NewsModel(models.Model):
    id = models.AutoField(max_length=5, primary_key = True)
    title = models.CharField(max_length = 80)
    author = models.CharField(max_length=15)
    url = models.CharField(max_length = 400)
    comments = models.CharField(max_length = 5)
    points = models.CharField(max_length = 5)
    label = models.CharField(max_length = 10)

class Users(models.Model):
    id = models.AutoField(max_length=5, primary_key = True)
    username = models.CharField(max_length = 15)
    password = models.CharField(max_length = 20)
    news_labeled =  models.CharField(max_length = 4000)
    favorite = models.CharField(max_length = 400)
