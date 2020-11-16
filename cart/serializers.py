from rest_framework import serializers
from .cart import Cart


class CartSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        model = Cart
        fields = '__all__'

