from django_filters import rest_framework as filters

from .models import TransactionHistory


# 거래내역 필터 / djnago-filter 사용 / 필터링 조건을 설정 URL 참조 부탁드립니다
# https://heokknkn.tistory.com/48
class TransactionHistoryFilter(filters.FilterSet):

    # 최소 금액 필터 (transaction_amount >= 입력값)
    min_amount = filters.NumberFilter(field_name="transaction_amount", lookup_expr="gte")
    # 최대 금액 필터 (transaction_amount <= 입력값)
    max_amount = filters.NumberFilter(field_name="transaction_amount", lookup_expr="lte")
    # 시작일 필터 (transaction_date >= 입력값)
    date_from = filters.DateTimeFilter(field_name="transaction_date", lookup_expr="gte")
    # 종료일 필터 (transaction_date <= 입력값)
    date_to = filters.DateTimeFilter(field_name="transaction_date", lookup_expr="lte")

    class Meta:
        model = TransactionHistory
        fields = [
            "deposit_withdrawal_type",  # 입출금 타입으로 필터링
            "transaction_type",  # 거래 타입으로 필터링
            "min_amount",
            "max_amount",  # 금액 범위로 필터링
            "date_from",
            "date_to",  # 날짜 범위로 필터링
        ]
