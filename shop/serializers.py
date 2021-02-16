from rest_framework import serializers
from .models import Category, Product
from comment.models import Comment
from comment.api.serializers import CommentSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'slug', 'image_1', 'alt_1',
                  'image_2', 'alt_2', 'image_3',  'alt_3', 'image_4', 'alt_4', 'image_5', 'alt_5',
                  'description', 'attribute', 'price', 'available', 'created', 'updated',
                  'popular', 'discount', 'comments']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

    def get_comments(self, obj):
        comments_qs = Comment.objects.filter_parents_by_object(obj).order_by('posted')
        return CommentSerializer(comments_qs, many=True).data

    def get_category(self, obj):
        return [c.name for c in obj.category.all()]

