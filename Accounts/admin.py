from django.contrib import admin
from .models import User, PhoneOTP, Address
from django.contrib.auth.models import Group


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'first_name', 'last_name', 'email', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'is_active')
    search_fields = ('phone', 'full_name')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'province', 'city', 'post_code')
    search_fields = ('user',)


admin.site.register(PhoneOTP)
admin.site.unregister(Group)
