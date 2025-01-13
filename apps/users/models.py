import random
from django.db import models
from datetime import timedelta
from django.utils import timezone
from apps.common.models import BaseModel
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser, UserManager, Permission



NEW, CODE_VERIFIED = ('new', 'code_verified',)
PHONE_EXPIRE = 2

class UserConfirmation(models.Model):
    code = models.CharField(max_length=4)
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='verify_code')
    expiration_time = models.DateTimeField(null=True)
    is_confirmation = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expiration_time = timezone.now() + timedelta(minutes=PHONE_EXPIRE)
        super(UserConfirmation, self).save(*args, **kwargs)

class AbstractUserManager(UserManager):
    def _create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError("The given phone number must be set")

        user = self.model(phone=phone, *extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('auth_status', 'code_verified')

        if extra_fields.setdefault('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.setdefault('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self._create_user(phone, password, **extra_fields)

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)


class User(AbstractUser, BaseModel):
    REQUIRED_FIELDS = []
    email = None
    username = None

    AUTH_STATUS = (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
    )

    phone = PhoneNumberField(unique=True, verbose_name=_("Phone"))
    auth_status = models.CharField(max_length=20, choices=AUTH_STATUS, default=NEW, verbose_name=_("Auth status"))
    objects = UserManager()
    USERNAME_FIELD = 'phone'

    class Meta:
        verbose_name = _("User")

    def __str__(self):
        return f"{self.phone} || {self.first_name}"

    def create_code_verify(self):
        code = "".join(str(random.randint(0, 100)%10) for _ in range(4))
        if hasattr(self, 'verify_code'):
            user_confirmation = self.verify_code
            user_confirmation.code = code
            user_confirmation.is_confirmed = False
            user_confirmation.expiration_time = timezone.now() + timedelta(minutes=PHONE_EXPIRE)
            user_confirmation.save()
        else:
            UserConfirmation.objects.create(user=self, code=code)
        return code

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


def __str__(self):
    return f"{self.name}"

Permission.__str__  = __str__


