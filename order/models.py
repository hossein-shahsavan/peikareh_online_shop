from django.db import models
from django.conf import settings
from shop.models import Product
from Accounts.models import Address


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='orders')
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    # products = models.ManyToManyField(OrderItem)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='addresses')
    created_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(null=True, blank=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.full_name

    def total_price(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_final_price()
        return total


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_item_price(self):
        return self.quantity * self.product.price

    def get_total_discount_item_price(self):
        return self.quantity * self.product.discount

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.product.discount:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()



