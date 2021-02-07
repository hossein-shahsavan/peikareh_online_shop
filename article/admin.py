from django.contrib import admin
from .models import Article


# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('article_title', 'show', 'created')
    list_editable = ('show',)
    list_filter = ('show', 'created')
    search_fields = ('article_title',)
    prepopulated_fields = {'slug': ('article_title',)}
