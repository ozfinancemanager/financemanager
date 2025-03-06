from rest_framework import serializers

from .models import Account, TransactionHistory


# 거래 내역 시리얼라이저
class TransactionHistorySerializer(serializers.ModelSerializer):
    # 계좌 번호 (읽기 전용)
    account_number = serializers.CharField(source="account.account_number", read_only=True)
    # 은행 코드 (읽기 전용)
    bank_code = serializers.CharField(source="account.bank_code", read_only=True)
    # 입출금 타입과 거래 타입의 표시 이름 (읽기 전용)
    deposit_withdrawal_type_display = serializers.CharField(
        source="get_deposit_withdrawal_type_display", read_only=True
    )
    transaction_type_display = serializers.CharField(source="get_transaction_type_display", read_only=True)

    # 거래 후 잔액 (읽기 전용)
    # 필드 일단 다 넣어뒀거든요? 나중에 필요없는 필드는 제거해도 무방합니다
    class Meta:
        model = TransactionHistory
        fields = [
            "id",
            "account",
            "account_number",
            "bank_code",
            "transaction_amount",
            "after_balance",
            "transaction_detail",
            "deposit_withdrawal_type",
            "deposit_withdrawal_type_display",
            "transaction_type",
            "transaction_type_display",
            "transaction_date",
        ]
        read_only_fields = ["id", "after_balance", "transaction_date"]


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "user", "account_number", "bank_code", "account_type", "balance"]

    def create(self, validated_data):
        return Account.objects.create(**validated_data)
