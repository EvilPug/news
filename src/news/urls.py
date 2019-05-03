from django.urls import path

from . import views

app_name = 'news'

urlpatterns = [
    path('', views.index, name='index'),
    path('favorite/', views.favorite, name='favorite'),
    path('add_label/', views.add_label, name='add_label'),
    path('add_favorite/', views.add_favorite, name='add_favorite'),
    path('update_news/', views.update_news, name='update_news'),
    path('recommendations/', views.recommendations, name='recommendations'),
]
