from rest_framework import serializers
from .models import Category, Product, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ['id', 'user', 'product', 'parent', 'body', 'created']


class CommentSerializer(serializers.ModelSerializer):
    loadParent = serializers.SerializerMethodField("loadPrentData")

    def loadPrentData(self, comment):
        comments = Comment.objects.filter(parent=comment)
        comments_ser = CommentSerializer(comments, many=True).data
        return comments_ser

    class Meta:
        model = Comment
        fields = ['id', 'user', 'product', 'parent', 'body', 'created', 'loadParent']


# class ProductSerializer(serializers.ModelSerializer):
#     comments = CommentSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Product
#         fields = ['id', 'category', 'name', 'slug', 'image_1',
#                   'image_2', 'image_3', 'image_4', 'image_5',
#                   'description', 'price', 'available', 'created', 'updated', 'comments']
#         lookup_field = 'slug'
#         extra_kwargs = {
#             'url': {'lookup_field': 'slug'}
#         }


class ProductSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField("loadProductComments")

    def loadProductComments(self, _product):
        _comments = Comment.objects.filter(product=_product, parent__isnull=True)
        _comments_ser = CommentSerializer(_comments, many=True, read_only=True).data
        return _comments_ser

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'slug', 'image_1',
                  'image_2', 'image_3', 'image_4', 'image_5',
                  'description', 'price', 'available', 'created', 'updated', 'comments']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
