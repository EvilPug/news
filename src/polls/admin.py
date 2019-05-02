from django.contrib import admin
from polls.models import NewsModel
from accounts.models import User

admin.site.register(NewsModel)
admin.site.register(User)
