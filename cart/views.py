from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .cart import Cart
from shop.models import Product
from .serializers import CartSerializer


@api_view()
def detail(request):
    cart = Cart(request)
    serializer = CartSerializer(data=cart)
    serializer.is_valid()
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    serializer = CartSerializer(data=request.POST)
    if serializer.is_valid():
        cart.add(product=product, quantity=serializer.validated_data['quantity'])
    return redirect('cart:detail')


@api_view()
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:detail')

