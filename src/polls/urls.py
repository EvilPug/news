from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('test/', views.admin, name='admin'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('favorite/', views.favorite, name='favorite'),
    path('add_label/', views.add_label, name='add_label'),
    path('update_news/', views.update_news, name='update_news'),
    path('recommendations/', views.recommendations, name='recommendations'),
]
