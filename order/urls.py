from django.urls import path
from .views import AddToCartView, OrderDetailView, OrderItemDeleteView, OrderQuantityUpdateView


app_name = 'order'
urlpatterns = [
    path('add_to_cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/delete/<pk>/', OrderItemDeleteView.as_view(), name='item_delete'),
    path('cart/update_quantity/', OrderQuantityUpdateView.as_view(), name='update_quantity'),
    path('cart/', OrderDetailView.as_view(), name='cart'),

]