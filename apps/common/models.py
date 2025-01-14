import os
from django.db import models
from decimal import Decimal
from django.dispatch import receiver
from apps.common.slug import unique_slugify
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_migrate, post_delete


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    image = models.ImageField(upload_to='category/', null=True, blank=True, verbose_name=_("Image"))
    icon = models.ImageField(upload_to='icon/', null=True, blank=True, max_length=55, verbose_name=_("Icon"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))
    top = models.BooleanField(default=True, verbose_name=_("Top category"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children',
                               verbose_name=_("Parent"))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ('oder',)

    def save(self, *args, **kwargs):
        if not self.pk:
            unique_slugify(self, self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.parent.title} || {self.title}" if self.parent else self.title


class Product(BaseModel):
    title = models.CharField(max_length=255, db_index=True, verbose_name=_("Title"))
    price = models.DecimalField(max_digits=100, max_length=2, verbose_name=_("Price"))
    price_uzs = models.DecimalField(max_digits=100, max_length=2, null=True, verbose_name=_("Price in UZS"))
    discount = models.PositiveIntegerField(default=0, verbose_name=_("Discount"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    view_count = models.PositiveIntegerField(default=0, verbose_name=_("View Count"))
    video_url = models.URLField(default='image.jfif', null=True, blank=True, verbose_name=_("Video Url"))
    body = RichTextUploadingField(default='good', verbose_name=_("Body"))
    on_sale = models.BooleanField(default=True, verbose_name=_("On Sale"))
    is_many = models.BooleanField(default=True, verbose_name=_("Can you sell more?"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products",
                                 limit_choices_to={'parent_isnull': False}, verbose_name=_("Category"))

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    @property
    def category_name(self):
        return self.category.title

    @property
    def first_image(self):
        return self.galleries.first().image
