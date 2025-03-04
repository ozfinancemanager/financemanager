from typing import Any, Type, cast

from django.contrib.auth import get_user_model
from django.test import TestCase

from finance.models import Account, CustomUser, TransactionHistory

User = cast(Type[CustomUser], get_user_model())  # settings.AUTH_USER_MODEL 설정된 모델 불러옴


class CustomUserModelTest(TestCase):
    def setUp(self) -> None:
        # Given
        self.user = User.objects.create_user(  # 유저 인스턴스 생성
            email="test@test.com",
            password="testpassword@",
            nickname="testnickname",
            name="test",
            phone_number="01012345678",
        )

    # When Then
    def test_custom_user_create(self) -> None:
        self.assertEqual(self.user.email, "test@test.com")  # user.email 과 test@test.com이 같은지 확인
        self.assertTrue(self.user.check_password("testpassword@"))  # 비밀번호가 올바르게 구성되었는지 확인
        self.assertEqual(self.user.nickname, "testnickname")  # 닉네임이 같은지 확인


class AccountModelTest(TestCase):
    def setUp(self) -> None:
        # Given
        self.user = User.objects.create_user(  # 유저 인스턴스 생성  -> ForeignKey 연결로 인해 생성함
            email="test@test.com",
            password="testpassword@",
            nickname="testnickname",
            name="testname",
            phone_number="01012345678",
        )
        self.account = cast(Any, Account).objects.create(
            user=self.user, account_number="1234567894561", bank_code="001", account_type="테스트은행", balance=10000.00
        )

    # When Then
    def test_account_create(self) -> None:
        self.assertEqual(
            self.account.user, self.user
        )  # account.user와 user가 맞는지 확인 => ForeignKey한 정보 일치한지 확인
        self.assertEqual(self.account.account_number, "1234567894561")  # 계좌번호가 맞는지 확인
        expected_str = f"{self.account.bank_code} - {self.account.account_number}"  # 예상 문자열 포맷이 일치한지 확인
        self.assertEqual(str(self.account), expected_str)


class TransactionHistoryModelTest(TestCase):
    def setUp(self) -> None:
        # Given: CustomUser와 해당 Account 인스턴스 생성
        self.user = User.objects.create_user(  # 유저 인스턴스 생성  -> Account ForeignKey 연결로 인해 생성함
            email="test@test.com",
            password="testpassword@",
            nickname="testnickname",
            name="test",
            phone_number="01012345678",
        )
        self.account = cast(
            Any, Account
        ).objects.create(  # 계좌정보 인스턴스 생성  -> transaction ForeignKey 연결로 인해 생성함
            user=self.user, account_number="1234567894561", bank_code="001", account_type="테스트은행", balance=10000.00
        )
        # Given
        self.transaction = cast(Any, TransactionHistory).objects.create(  # 거래 정보 인스턴스 생성
            account=self.account,
            transaction_amount=4500.00,
            after_balance=5500.00,
            transaction_detail="GS25",
            deposit_withdrawal_type="출금",
            transaction_type="카드결제",
        )

    def test_transaction_history_creation(self) -> None:
        # When Then
        self.assertEqual(self.transaction.account, self.account)  # ForeignKey한 정보 일치한지 확인
        self.assertEqual(self.transaction.transaction_amount, 4500.00)  # 거래 금액이 4500원이 맞는지 확인
        expected_str = f"{self.transaction.deposit_withdrawal_type} - {self.transaction.transaction_amount} - {self.transaction.after_balance}"  # 예상 문자열 포맷이 일치한지 확인
        self.assertEqual(str(self.transaction), expected_str)
