from django.urls import path, re_path
from . import views


app_name = 'articles'
urlpatterns = [
    path('', views.ArticleList.as_view(), name='article_list'),
    path('new_articles/', views.NewestArticles.as_view(), name='new_articles'),
    re_path(r'(?P<slug>[-\w]+)/', views.ArticleDetail.as_view(), name='article_detail'),

]
