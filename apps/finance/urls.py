from django.urls import path
from apps.finance.views import BuyGoldApiView,SellGoldApiView,TransactionListView
urlpatterns = [
    path('buy', BuyGoldApiView.as_view(), name='buy_gold'),
    path('sell', SellGoldApiView.as_view(), name='sell_gold'),
    path('user/<uuid:user_id>', TransactionListView.as_view(), name='transaction-list'),

]