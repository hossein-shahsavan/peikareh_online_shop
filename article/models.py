from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Article(models.Model):
    page_title = models.CharField(max_length=200, null=True, blank=True)
    article_title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='articles_pic/%Y/%m/%d/')
    content = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.article_title

    class Meta:
        ordering = ('-created',)
