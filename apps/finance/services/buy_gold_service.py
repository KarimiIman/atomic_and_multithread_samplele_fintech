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


class BuyGoldService:

    def __init__(self, user, wallet, amount):
        self.user = user
        self.wallet = wallet
        self.amount = amount

    @staticmethod
    def calculate_gold_amount(amount):
        return amount / PRICE_PER_GRAM

    def buy_gold(self):
        try:
            with trans.atomic():
                wallet = Wallet.objects.select_for_update().get(id=self.wallet.id)
                business_asset = BusinessAsset.objects.select_for_update().first()
                if not business_asset:
                    raise ValueError("Business asset is not configured.")

                total_gold_grams = self.calculate_gold_amount(self.amount)
                print("tatal_gold_gram :", total_gold_grams)
                if business_asset.gold_balance < total_gold_grams:
                    raise ValueError("Insufficient gold in business asset.")

                if wallet.rial_balance < self.amount:
                    raise ValueError("Insufficient wallet balance.")
                print("self.amount :", self.amount)
                print("rial_balance1 :", wallet.rial_balance - self.amount)

                wallet.rial_balance -= self.amount
                wallet.gold_balance += total_gold_grams
                wallet.save()
                print("rial_balance2 :", business_asset.rial_balance - self.amount)

                business_asset.rial_balance += self.amount
                business_asset.gold_balance -= total_gold_grams
                business_asset.save()

                transaction = Transaction.objects.create(
                    user=self.user,
                    transaction_type=Transaction.TRANSACTION_TYPES.BUY,
                    rial_amount=self.amount,
                    gold_amount=total_gold_grams,
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
