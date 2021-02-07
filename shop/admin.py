from django.contrib import admin
from .models import Category, Product


admin.site.register(Category)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount', 'available', 'popular', 'created')
    list_filter = ('available', 'popular', 'created')
    list_editable = ('price', 'available', 'discount', 'popular')
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('category',)
    search_fields = ('name', 'price')
