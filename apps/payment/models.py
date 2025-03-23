from django.db import models
from django.conf import settings
from django.db.models import Sum
from .utils import check_quantity
from django.dispatch import receiver
from apps.common.models import BaseModel
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models.signals import post_migrate, pre_save
from phonenumber_field.serializerfields import PhoneNumberField



phone_validator = RegexValidator(
    regex=r"^\+998\d{9}$", message=_("Phone number don't match"), code='invalid'
)


class Branch(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Branch Name"))
    description = models.CharField(max_length=255, verbose_name=_("Branch Description"), null=True, blank=True)
    longitude = models.FloatField(verbose_name=_("Longitude"), null=True, blank=True)
    latitude = models.FloatField(verbose_name=_("Latitude"), null=True, blank=True)
    location = models.URLField(max_length=300000, verbose_name=_("Location URL"), null=True)
    support_phone = models.CharField(max_length=255, verbose_name=_("Support Phone"), validators=[phone_validator],
                                     null=True)
    archive = models.BooleanField(default=False, verbose_name=_("Archive"))

    @property
    def value(self):
        return str(self.pk)

    class Meta:
        verbose_name = _("Branch")
        verbose_name_plural = _("Branches")

    def __str__(self):
        return self.name


class Order(BaseModel):
    class OrderStatus(models.TextField):
        PENDING = 'pending', _('Pending')
        APPROVED = 'approved', _('Approved')
        CANCELLED = 'cancelled', _('Cancelled')

    class ProcessStatus(models.TextField):
        NEW = 'new', _('New')
        IN_COURIER = 'in_courier', _('In courier')
        DELIVERED = 'delivered', _('Delivered')

    class OrderType(models.TextField):
        DELIVERY = 'delivery', _('Delivery')
        TAKE_AWAY = 'take_away', _('Take away')

    class ProviderType(models.TextField):
        CLICK = 'click', _('Click')
        PAYME = 'payme', _('Payme')
        PAYZE = 'payze', _('Payze')
        CASH = 'cash', _('Cash')

    phone_number = PhoneNumberField(verbose_name=_('Phone number'))
    customer_name = models.CharField(max_length=255, verbose_name=_("Customer Name"), null=True)
    address = models.CharField(max_length=255, verbose_name=_("Address"), null=True, blank=True)
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    total_amount = models.PositiveIntegerField(default=1, verbose_name=_("Total Amount"))
    longitude = models.FloatField(verbose_name=_("Longitude"), null=True, blank=True)
    latitude = models.FloatField(verbose_name=_("Latitude"), null=True, blank=True)
    user = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='orders', verbose_name=_("User"))
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='orders', verbose_name=_("Branch"),
                               null=True)
    status = models.CharField(max_length=255, choices=OrderStatus.choices, default=OrderType.DELIVERY,
                              verbose_name=_("Status"))
    order_type = models.CharField(max_length=255, choices=OrderType.choices, default=OrderType.DELIVERY,
                                  verbose_name=_("Order Type"))
    process = models.CharField(max_length=255, choices=ProcessStatus.choices, default=ProcessStatus.NEW,
                               verbose_name=_("Process Type"))
    provider = models.CharField(max_length=255, choices=ProviderType.choices, default=ProviderType.CASH,
                                verbose_name=_("Provider Type"))

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"{dict(self.OrderType.choices)[self.order_type]} || {self.id}"

    def clean(self):
        if self.pk:
            old_order = Order.objects.get(pk=self.pk)
            if self.status == 'approved' != old_order.status and not check_quantity(self):
                raise ValidationError(_('There is a shortage of products in the warehouse'))

    @property
    def amounts(self):
        amount = self.product_orders.aggregate(Sum('amount'))['amount__sum'] or 0
        return {
            "product_amount": amount,
            "shipping_amount": self.total_amount - amount
        }

    @property
    def status_ln(self):
        status_choice = dict(Order.OrderStatus.choices)
        return status_choice[self.status]

    @property
    def order_type_ln(self):
        order_type_ls = dict(Order.OrderType.choices)
        return order_type_ls[self.order_type]

    @property
    def process_ln(self):
        process_choice = dict(Order.ProcessStatus.choices)
        return process_choice[self.process]

    def save(self, *args, **kwargs):
        if self.pk:
            old_order = Order.objects.get(pk=self.pk)
            if self.status == 'approved' and old_order.status != 'approved':
                for product_count in self.product_orders.all().select_related('product'):
                    product_count.product.quantity -= product_count.quantity
                    product_count.product.save()
        super().save(*args, **kwargs)


class ProductCountOrder(BaseModel):
    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"))
    amount = models.PositiveIntegerField(verbose_name=_("Amount"))
    product = models.ForeignKey('common.Product', on_delete=models.PROTECT, related_name='product_orders',
                                verbose_name=_("Product"))
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='product_orders', verbose_name=_("Order"))

    class Meta:
        verbose_name = _("Product count order")
        verbose_name_plural = _("Product count orders")

    @property
    def price(self):
        return self.amount / self.quantity


class ApplicationForMoreProduct(BaseModel):
    quantity = models.PositiveIntegerField(verbose_name=_("quantity"))
    phone_number = models.CharField(max_length=20, verbose_name=_("Phone number"))
    customer_name = models.CharField(max_length=255, verbose_name=_("Customer Name"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='applications')
    products = models.ForeignKey('common.Product', on_delete=models.PROTECT, related_name='applications',
                                 verbose_name=_("Product"))

    class Meta:
        verbose_name = _("Application for product")
        verbose_name_plural = _("Application for products")


class Settings(BaseModel):
    shipping_cost = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0, verbose_name=_('Shipping cost in USD'),
        help_text=_('The shipping cost is the amount charged to deliver the order in USD')
    )
    minute = models.PositiveIntegerField(
        default=0, verbose_name=_('Minute'),
        help_text=_('This is to show users who have logged in in the last few minutes')
    )
    usd_to_uzs_rate = models.DecimalField(
        max_digits=12, decimal_places=2,
        verbose_name=_('USD to UZS Exchange Rate'),
        help_text=_('Exchange rate from USD to UZS'),
    )
    last_updated = models.DateTimeField(
        auto_now=True, verbose_name=_('Last Updated'),
        help_text=_('The date and time when the exchange rate was last updated')
    )

    def __str__(self):
        return str(_('Settings for site configuration'))

    class Meta:
        verbose_name = _('Settings')
        verbose_name_plural = _('Settings')


@receiver(post_migrate)
def my_post_migrate_handler(sender, **kwargs):
    if not Settings.objects.all().exists():
        Settings.objects.create()

