from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'ordered_date',
                    'address',
                    'created_date',
                    'total_price'

                    ]
    list_display_links = ['user', 'address']
    list_filter = ['ordered', ]
    search_fields = [
        'user',
        'ref_code'
    ]
    inlines = (OrderItemInline,)


# admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderItem)
