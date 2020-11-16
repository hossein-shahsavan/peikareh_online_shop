from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Category, Product, Comment
from Accounts.models import User
from .serializers import ProductSerializer, CommentSerializer
from rest_framework import generics, permissions, status
from rest_framework import filters


class Home(generics.ListAPIView):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'category__name', 'description']


class RetrieveProductView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'slug'


@api_view(['POST'])
def AddComent(request, parent_id=None):
    parent = request.data.get("parent_id")
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        if parent is not None:
            comment = Comment.objects.create(user=request.user, product=serializer.validated_data['product'],
                                             parent_id=serializer.validated_data['parent'],
                                             body=serializer.validated_data['body'])
        else:
            comment = Comment.objects.create(user=request.user, product=serializer.validated_data['product'],
                                             body=serializer.validated_data['body'])

        comments_ser = CommentSerializer(comment,many=False, read_only=True).data
        return Response(comments_ser, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)










