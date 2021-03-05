from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment


class Category(models.Model):
    name = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, allow_unicode=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products')
    name = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, allow_unicode=True, unique=True)
    page_title = models.CharField(max_length=200, null=True, blank=True, help_text='used for seo')  # for seo
    page_description = models.TextField(null=True, blank=True, help_text='used for seo')  # for seo
    image_1 = models.ImageField(upload_to='products_pic/%Y/%m/%d/', null=True, blank=True)
    alt_1 = models.CharField(max_length=200, null=True, blank=True, help_text='used for seo')
    image_2 = models.ImageField(upload_to='products_pic/%Y/%m/%d/', null=True, blank=True)
    alt_2 = models.CharField(max_length=200, null=True, blank=True, help_text='used for seo')
    image_3 = models.ImageField(upload_to='products_pic/%Y/%m/%d/', null=True, blank=True)
    alt_3 = models.CharField(max_length=200, null=True, blank=True, help_text='used for seo')
    image_4 = models.ImageField(upload_to='products_pic/%Y/%m/%d/', null=True, blank=True)
    alt_4 = models.CharField(max_length=200, null=True, blank=True, help_text='used for seo')
    image_5 = models.ImageField(upload_to='products_pic/%Y/%m/%d/', null=True, blank=True)
    alt_5 = models.CharField(max_length=200, null=True, blank=True, help_text='used for seo')
    description = models.TextField(null=True, blank=True)
    attribute = models.JSONField(null=True, blank=True,
                                 help_text='in this format: {"key" : "value", "key2" : "value2"}')
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(null=True, blank=True)
    available = models.BooleanField(default=True)
    popular = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    comments = GenericRelation(Comment)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name
