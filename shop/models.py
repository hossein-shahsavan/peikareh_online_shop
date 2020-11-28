from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment


class Category(models.Model):
    name = models.CharField(max_length=400)

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
    image_1 = models.ImageField(upload_to='products_pic/%Y/%m/%d/', null=True, blank=True)
    image_2 = models.ImageField(upload_to='products_pic/%Y/%m/%d/', null=True, blank=True)
    image_3 = models.ImageField(upload_to='products_pic/%Y/%m/%d/', null=True, blank=True)
    image_4 = models.ImageField(upload_to='products_pic/%Y/%m/%d/', null=True, blank=True)
    image_5 = models.ImageField(upload_to='products_pic/%Y/%m/%d/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
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







