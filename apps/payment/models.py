from django.db import models
from phonenumber_field.serializerfields import PhoneNumberField

from .utils import check_quantity
from apps.common.models import BaseModel
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

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
