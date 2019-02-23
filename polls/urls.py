from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.admin, name='admin'),
    path('add_label/', views.add_label, name='add_label'),
    path('update_news/', views.update_news, name='update_news'),
	path('recommendations/', views.recommendations, name='recommendations'),
]
