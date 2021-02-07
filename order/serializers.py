from rest_framework import serializers
from .models import Order, OrderItem
from shop.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'product',
            'quantity',
            'final_price'
        )

    def get_product(self, obj):
        return ProductSerializer(obj.product).data

    def get_final_price(self, obj):
        return obj.get_final_price()


class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'order_items',
            'total',
        )

    def get_order_items(self, obj):
        return OrderItemSerializer(obj.products.all(), many=True).data

    def get_total(self, obj):
        return obj.total_price()


