from django.db import transaction as trans
from apps.finance.models import Transaction
from apps.notifications.services.send_notif_services import NotificationService
from apps.account.models import Wallet
from apps.finance.models import BusinessAsset
from django.contrib.auth import get_user_model
from apps.finance.constant import PRICE_PER_GRAM
User = get_user_model()
import logging

logger = logging.getLogger('custom')


class SellGoldService:

    def __init__(self, user, wallet, gold_weight_gram):
        self.user = user
        self.wallet = wallet
        self.gold_weight_gram = gold_weight_gram

    @staticmethod
    def calculate_rial_amount(gold_weight_gram):
        return round(gold_weight_gram * PRICE_PER_GRAM, 4)

    def sell_gold(self):
        try:
            with trans.atomic():
                wallet = Wallet.objects.select_for_update().get(id=self.wallet.id)
                business_asset = BusinessAsset.objects.select_for_update().first()
                if not business_asset:
                    raise ValueError("Business asset is not configured.")

                if wallet.gold_balance < self.gold_weight_gram:
                    raise ValueError("Insufficient wallet balance.")

                total_rial_amount = self.calculate_rial_amount(self.gold_weight_gram)
                if business_asset.rial_balance < total_rial_amount:
                    raise ValueError("Insufficient rial in business asset.")

                print("--------->",total_rial_amount)
                wallet.rial_balance += total_rial_amount
                wallet.gold_balance -= self.gold_weight_gram
                wallet.save()

                business_asset.rial_balance -= total_rial_amount
                business_asset.gold_balance += self.gold_weight_gram
                business_asset.save()

                transaction = Transaction.objects.create(
                    user=self.user,
                    transaction_type=Transaction.TRANSACTION_TYPES.SELL,
                    rial_amount=total_rial_amount,
                    gold_amount=self.gold_weight_gram,
                    price_per_gram=PRICE_PER_GRAM,
                    status=Transaction.TRANSACTION_STATUS.COMPLETED
                )
                NotificationService(
                    recipient=self.user,
                    message=f"Transaction with ID {transaction.id} successfully performed"
                ).send_notification()
                return True, transaction

        except Exception as e:
            return False, str(e)
