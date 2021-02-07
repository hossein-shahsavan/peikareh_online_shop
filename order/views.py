from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import Http404
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from shop.models import Product
from .models import OrderItem, Order
from .serializers import OrderItemSerializer, OrderSerializer


class OrderQuantityUpdateView(APIView):
    """
    this view is just for decreasing the quantity of order item.
    for increasing the quantity should use the add to cart view.
    """

    def post(self, request, *args, **kwargs):
        slug = request.data.get('slug', None)
        if slug is None:
            return Response({"message": "Invalid data"}, status=HTTP_400_BAD_REQUEST)
        product = get_object_or_404(Product, slug=slug)
        order_qs = Order.objects.filter(
            user=request.user,
            ordered=False
        )
        if order_qs.exists():
            order = order_qs[0]
            # check if the order product is in the order
            if order.products.filter(product__slug=product.slug).exists():
                order_item = OrderItem.objects.filter(
                    product=product,
                    user=request.user,
                    order=order,
                    ordered=False
                )[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                else:
                    order_item.delete()
                    # order.products.remove(order_item)
                return Response(status=HTTP_200_OK)
            else:
                return Response({"message": "This item was not in your cart"}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "You do not have an active order"}, status=HTTP_400_BAD_REQUEST)


class OrderItemDeleteView(DestroyAPIView):
    """
    this view is for deleting a single order_item from the cart.
    not for increase or decrease the quantity.
    """
    permission_classes = (IsAuthenticated,)
    queryset = OrderItem.objects.all()


class AddToCartView(APIView):
    def post(self, request, *args, **kwargs):
        slug = request.data.get('slug', None)
        if slug is None:
            return Response({"message": "Invalid request"}, status=HTTP_400_BAD_REQUEST)
        product = get_object_or_404(Product, slug=slug)

        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            order_item_qs = OrderItem.objects.filter(
                product=product,
                user=request.user,
                order=order,
                ordered=False
            )
            order_item = order_item_qs
            if order_item is not None and order.products.filter(product__slug=product.slug).exists():

                order_item = order_item_qs[0]
                order_item.quantity += 1
                order_item.save()
                return Response(status=HTTP_200_OK)

            else:
                orderItem = OrderItem.objects.create(
                    product=product,
                    user=request.user,
                    order=order,
                    ordered=False
                )
                orderItem.save()
                # order.products.add(order_item)
                return Response(status=HTTP_200_OK)

        else:
            # ordered_date = timezone.now()
            order = Order.objects.create(user=request.user)
            order.save()
            # order.products.add(order_item)
            orderItem = OrderItem.objects.create(
                product=product,
                user=request.user,
                order=order,
                ordered=False
            )
            orderItem.save()
            return Response(status=HTTP_200_OK)


class OrderDetailView(RetrieveAPIView):  # customer cart.
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            return order
        except ObjectDoesNotExist:
            raise Http404("You do not have an active order")
            # return Response({"message": "You do not have an active order"}, status=HTTP_400_BAD_REQUEST)
