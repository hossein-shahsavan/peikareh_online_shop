from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group
from.models import Profile

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'is_active')
    search_fields = ('email',)


admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.unregister(Group)
