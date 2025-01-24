from django.db import models
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


