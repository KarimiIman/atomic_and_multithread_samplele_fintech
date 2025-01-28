from django.core.exceptions import ValidationError
from rest_framework import serializers
from apps.account.models import User
from apps.finance.models import Transaction

class BuyGoldRequestSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(required=True)
    amount = serializers.DecimalField(max_digits=30, decimal_places=4, required=True)

    def validate(self, data):
        user_id = data.get('user_id')
        amount = data.get('amount')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({"user_id": "User with the given ID does not exist."})

        wallet = getattr(user, 'wallet', None)
        if wallet is None:
            raise serializers.ValidationError({"wallet": "User does not have a wallet."})

        if wallet.rial_balance <= amount:
            raise serializers.ValidationError({"wallet_balance": "Wallet balance is insufficient."})
        data['user'] = user
        data['wallet'] = wallet
        return data


class TransactionResponseSerializer(serializers.Serializer):
    transaction_id = serializers.IntegerField(source='id')
    user_id = serializers.IntegerField(source='user.id')
    gold_weight_gram = serializers.DecimalField(max_digits=10, decimal_places=6, source='gold_amount')
    amount_rial = serializers.DecimalField(max_digits=20, decimal_places=4, source='rial_amount')
    price_per_gram = serializers.DecimalField(max_digits=20, decimal_places=4)
    status = serializers.CharField()


class SellGoldRequestSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(required=True)
    gold_weight_gram = serializers.DecimalField(max_digits=30, decimal_places=6, required=True)

    def validate(self, data):
        user_id = data.get('user_id')
        gold_weight_gram = data.get('gold_weight_gram')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({"user_id": "User with the given ID does not exist."})

        wallet = getattr(user, 'wallet', None)
        if wallet is None:
            raise serializers.ValidationError({"wallet": "User does not have a wallet."})

        if wallet.gold_balance <= gold_weight_gram:
            raise serializers.ValidationError({"wallet_balance": "Wallet balance is insufficient."})
        data['user'] = user
        data['wallet'] = wallet
        return data





class TransactionModelSerializer(serializers.ModelSerializer):
    transaction_id = serializers.IntegerField(source='id')
    type = serializers.CharField(source='transaction_type')
    amount_rial = serializers.DecimalField(source='rial_amount', max_digits=30, decimal_places=4)
    gold_weight_gram = serializers.DecimalField(source='gold_amount', max_digits=10, decimal_places=6)
    date = serializers.DateTimeField(source='create_time', format='%Y-%m-%d')

    class Meta:
        model = Transaction
        fields = [
            'transaction_id', 'type', 'amount_rial', 'gold_weight_gram',
            'price_per_gram', 'date', 'status'
        ]