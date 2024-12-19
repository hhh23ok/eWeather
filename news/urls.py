from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('articles/', views.articles, name='articles')
]
