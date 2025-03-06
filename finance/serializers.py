from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "user", "account_number", "bank_code", "account_type", "balance"]

    def create(self, validated_data):
        return Account.objects.create(**validated_data)
