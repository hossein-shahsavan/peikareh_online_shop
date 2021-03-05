from .models import Article
from .serializers import ArticleSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny


class ArticleList(generics.ListAPIView):
    queryset = Article.objects.filter(show=True)
    serializer_class = ArticleSerializer
    permission_classes = (AllowAny,)


class ArticleDetail(generics.RetrieveAPIView):
    queryset = Article.objects.filter(show=True)
    serializer_class = ArticleSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'slug'


class NewestArticles(generics.ListAPIView):
    queryset = Article.objects.filter(show=True).order_by('-created')[:4]
    serializer_class = ArticleSerializer
    permission_classes = (AllowAny,)


