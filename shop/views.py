from django.shortcuts import render
from .models import Product
from .serializers import ProductSerializer
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import ProductFilter


class Home(generics.ListAPIView):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)


class search(generics.ListAPIView):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class= ProductFilter
    search_fields = ['name', 'category__name', 'description']


class RetrieveProductView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'slug'











