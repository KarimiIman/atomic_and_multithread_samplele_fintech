from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.models import BaseModel
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


class User(BaseModel, AbstractUser):
    def __str__(self):
        return self.username


class UserProfile(BaseModel):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('user'),
        unique=True
    )
    phone_number = models.CharField(
        db_index=True, max_length=16,
        validators=[RegexValidator(regex=r"^(0?9\d{9}|\+989\d{9})$")], verbose_name=_("phone number")
    )
    is_email_verified = models.BooleanField(default=False, verbose_name=_('email verified'), )
    is_phone_number_verified = models.BooleanField(default=False, verbose_name=_('phone number verified'), )

    @property
    def fullname(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return self.fullname


class Wallet(BaseModel):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='wallet')
    rial_balance = models.DecimalField(max_digits=20, validators=[MinValueValidator(0)], decimal_places=4,
                                       help_text="rial", default=0)
    gold_balance = models.DecimalField(max_digits=10, validators=[MinValueValidator(0)], decimal_places=6,
                                       help_text="gerame tala", default=0)

    def __str__(self):
        return f"Wallet of {self.user.username}"
