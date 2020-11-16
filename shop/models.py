from django.db import models
from django .conf import settings


class Category(models.Model):
    name = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True, verbose_name='slug (should be english)')

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products')
    name = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500,allow_unicode=True, unique=True)
    image_1 = models.ImageField(upload_to='products_pic/%Y/%m/%d/', null=True, blank=True)
    image_2 = models.ImageField(upload_to='products_pic/%Y/%m/%d/', null=True, blank=True)
    image_3 = models.ImageField(upload_to='products_pic/%Y/%m/%d/', null=True, blank=True)
    image_4 = models.ImageField(upload_to='products_pic/%Y/%m/%d/', null=True, blank=True)
    image_5 = models.ImageField(upload_to='products_pic/%Y/%m/%d/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True,blank=True, related_name='replys')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'

    class Meta:
        ordering = ('-created',)




