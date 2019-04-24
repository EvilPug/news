from django.contrib import admin
from .models import NewsModel, Users

admin.site.register(NewsModel)
admin.site.register(Users)
