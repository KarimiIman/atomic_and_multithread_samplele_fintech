from django.db import models
from utils.models import BaseModel
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from apps.account.models import User
from django.core.exceptions import ValidationError


class Transaction(BaseModel):
    class TRANSACTION_TYPES(models.TextChoices):
        INCREASE_CREDIT = 'INCREASE_CREDIT', _('increase credit')
        SELL = 'SELL', _('sell')
        BUY = 'BUY', _('buy')

    class TRANSACTION_STATUS(models.TextChoices):
        PENDING = 'PENDING', _('pending')
        COMPLETED = 'COMPLETED', _('completed')
        FAILED = 'FAILED', _('failed')

    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='transactions'
    )
    transaction_type = models.CharField(
        max_length=15,
        choices=TRANSACTION_TYPES.choices
    )
    rial_amount = models.DecimalField(max_digits=30, validators=[MinValueValidator(0)], decimal_places=4,
                                      help_text="rial", default=0)
    gold_amount = models.DecimalField(max_digits=10, validators=[MinValueValidator(0)], decimal_places=6,
                                      help_text="gerame tala", default=0)
    price_per_gram = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        help_text="price of gold per gram at transaction time"
    )
    status = models.CharField(
        max_length=10,
        choices=TRANSACTION_STATUS.choices,
        default=TRANSACTION_STATUS.PENDING,
        help_text="status of the transaction"
    )

    def clean(self):
        if self.transaction_type != self.TRANSACTION_TYPES.INCREASE_CREDIT and self.gold_amount <= 0:
            raise ValidationError(_("When buying or selling, a valid amount of gold must be specified."))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.rial_amount}"

    class Meta:
        ordering = ['-create_time', 'status']



class BusinessAsset(BaseModel):
    rial_balance = models.DecimalField(
        max_digits=30,
        decimal_places=4,
        validators=[MinValueValidator(0)],
        default=0,
        help_text="total cash"
    )
    gold_balance = models.DecimalField(
        max_digits=30,
        decimal_places=6,
        validators=[MinValueValidator(0)],
        default=0,
        help_text="total gold"
    )

    def __str__(self):
        return f"Business Asset - Rial: {self.rial_balance}, Gold: {self.gold_balance}g"
