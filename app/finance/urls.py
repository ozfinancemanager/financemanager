from django.urls import path

from .views import (
    AccountDeleteView,
    AccountDetailAPIView,
    AccountListCreateView,
    TransactionHistoryDetail,
    TransactionHistoryListCreate,
)

urlpatterns = [
    path("accounts/", AccountListCreateView.as_view(), name="account-create"),
    path("accounts/<int:pk>/", AccountDetailAPIView.as_view(), name="account-detail"),
    path("transactions/", TransactionHistoryListCreate.as_view(), name="transaction-list-create"),  # url 추가
    path("transactions/<int:pk>/", TransactionHistoryDetail.as_view(), name="transaction-detail"),  # url 추가
    path("accounts/<int:account_id>/delete/", AccountDeleteView.as_view(), name="account-delete"),
]
