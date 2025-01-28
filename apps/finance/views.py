from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as rest_status
from apps.finance.serializers import BuyGoldRequestSerializer, TransactionResponseSerializer, SellGoldRequestSerializer
from apps.finance.services.buy_gold_service import BuyGoldService
from apps.finance.services.sell_gold_service import SellGoldService
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from .models import Transaction, User
from apps.finance.serializers import TransactionModelSerializer
from concurrent.futures import ThreadPoolExecutor
from apps.finance.permissions import OnlyWalletOwnerWithOutBodyPermission,OnlyWalletOwnerWithBodyPermission
executor = ThreadPoolExecutor(max_workers=10)
import logging

logger = logging.getLogger('custom')


class BuyGoldApiView(APIView):
    permission_classes = [OnlyWalletOwnerWithBodyPermission]

    def post(self, request, *args, **kwargs):
        serializer = BuyGoldRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        wallet = serializer.validated_data['wallet']
        amount = serializer.validated_data['amount']

        service = BuyGoldService(user, wallet, amount)
        future = executor.submit(service.buy_gold)
        success, result = future.result()

        if success:
            response_serializer = TransactionResponseSerializer(result)
            return Response(response_serializer.data, status=rest_status.HTTP_201_CREATED)

        logger.error(f"Error occurred while processing buy gold for user: {user.id}. Error: {str(result)}")
        return Response({"message": result}, status=rest_status.HTTP_400_BAD_REQUEST)


class SellGoldApiView(APIView):
    permission_classes = [OnlyWalletOwnerWithBodyPermission]

    def post(self, request, *args, **kwargs):
        serializer = SellGoldRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        wallet = serializer.validated_data['wallet']
        gold_weight_gram = serializer.validated_data['gold_weight_gram']

        service = SellGoldService(user, wallet, gold_weight_gram)
        future = executor.submit(service.sell_gold)
        success, result = future.result()

        if success:
            response_serializer = TransactionResponseSerializer(result)
            return Response(response_serializer.data, status=rest_status.HTTP_201_CREATED)

        logger.error(f"Error occurred while processing sell gold for user: {user.id}. Error: {str(result)}")
        return Response({"message": result}, status=rest_status.HTTP_400_BAD_REQUEST)



class TransactionListView(ListAPIView):
    serializer_class = TransactionModelSerializer
    permission_classes = [OnlyWalletOwnerWithOutBodyPermission]
    def get_queryset(self):
        try:
            user = User.objects.get(id=self.kwargs.get('user_id'))
        except User.DoesNotExist:
            raise NotFound("User not found")
        return Transaction.objects.filter(user=user,status=Transaction.TRANSACTION_STATUS.COMPLETED)