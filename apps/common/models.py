import os
from django.db import models
from django.dispatch import receiver
from apps.common.slug import unique_slugify
from django.utils.translation import gettext_lazy as _
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
        ordering = ('order',)

    def save(self, *args, **kwargs):
        if not self.pk:
            unique_slugify(self, self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.parent.title} || {self.title}" if self.parent else self.title


class Product(BaseModel):
    title = models.CharField(max_length=255, db_index=True, verbose_name=_("Title"))
    price = models.DecimalField(max_digits=100, decimal_places=2, max_length=2, verbose_name=_("Price"))
    price_uzs = models.DecimalField(max_digits=100, decimal_places=2, max_length=2, null=True,
                                    verbose_name=_("Price in UZS"))
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

    def __str__(self):
        return self.title


class Gallery(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='galleries', verbose_name=_("Product"))
    image = models.ImageField(upload_to="gallery/", verbose_name=_("Image"))

    class Meta:
        verbose_name = _("Gallery")
        verbose_name_plural = _("Galleries")


class ProductCharacteristics(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="characteristics",
                                verbose_name=_(Product))
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    value = models.CharField(max_length=255, verbose_name=_("Value"))

    class Meta:
        verbose_name = _("Product Characteristic")
        verbose_name_plural = _("ProductCharacteristics")


class Banner(BaseModel):
    class BannerYtps(models.TextChoices):
        BANNER = 'banner', _('Banner')
        ADVERTISING = 'advertising', _('Advertising')

    title = models.CharField(max_length=255, null=True, verbose_name=_("Title"))
    image = models.ImageField(upload_to="banner/", verbose_name=_("Image"))
    url = models.URLField(null=True, blank=True, verbose_name=_("Banner URL"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    banner_type = models.CharField(choices=BannerYtps.choices, default=BannerYtps.BANNER,
                                   max_length=40, verbose_name=_("Banner Type"))

    class Meta:
        verbose_name = _("Banner")
        verbose_name_plural = _("Banners")
        ordering = ('order',)

    def __str__(self):
        return self.title


class Brand(BaseModel):
    image = models.ImageField(upload_to='brand/', verbose_name=_("Image"))
    name = models.CharField(max_length=255, verbose_name=_("Brand Name"))
    url = models.URLField(verbose_name=_("Brand URL"), null=True, blank=True)
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order number"))

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")
        ordering = ('order',)

    def __str__(self):
        return self.name


class Section(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Section Name"))
    code = models.CharField(max_length=255, verbose_name=_("Code"), null=True, unique=True)
    products = models.ManyToManyField(Product, related_name='product_sections',
                                      limit_choices_to={'on_sale': True, 'quantity__gt': 0}, blank=True)

    def save(self, *args, **kwargs):
        count = self.__class__.objects.all().count
        self.code = f"section_{count + 1}"
        super(Section, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Section")
        verbose_name_plural = _("Sections")


class Contact(BaseModel):
    full_name = models.CharField(max_length=255, verbose_name=_("Full Name"))
    phone_or_email = models.CharField(max_length=255, verbose_name=_("Phone or Email"))
    message = models.TextField(verbose_name=_("Message"), null=True, blank=True)

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")


class Country(BaseModel):
    country_nme = models.CharField(max_length=255, verbose_name=_("Country Name"))
    region = models.CharField(max_length=255, verbose_name=_("Region"))


class OnlineUser(BaseModel):
    ip_address = models.GenericIPAddressField(max_length=255, verbose_name=_("IP Address"), null=True, blank=True)
    country = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='online_users',
                                verbose_name=_("Online User"), null=True, blank=True)
    uuid = models.CharField(max_length=255, verbose_name=_("UUID"), null=True)
    is_authenticated = models.BooleanField(default=False, verbose_name=_("Authenticated"))
    quantity = models.PositiveIntegerField(default=0, verbose_name=_("Quantity"))


@receiver(post_migrate)
def my_post_migrate_handler(ender, **kwargs):
    sections = Section.objects.all()
    if sections.count() < 4:
        sections.delete()
        for i in range(4):
            Section.objects.create(name=f'Section {1 + i}', code=f'section_{i + 1}')


@receiver(post_delete, sender=Gallery)
def post_delete_handler_gallery(sender, instance, **kwargs):
    if os.path.exists(instance.image.path):
        os.remove(instance.image.path)


@receiver(post_delete, sender=Banner)
def post_delete_handler_banner(sender, instance, **kwargs):
    if os.path.exists(instance.image.path):
        os.remove(instance.image.path)


@receiver(post_delete, sender=Brand)
def post_delete_handler(sender, instance, **kwargs):
    if os.path.exists(instance.image.path):
        os.remove(instance.image.path)
