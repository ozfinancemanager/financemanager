from typing import Any, Optional, TypeVar

from django.contrib.auth.base_user import (  # BaseUserManager 임포트
    AbstractBaseUser,
    BaseUserManager,
)
from django.contrib.auth.models import PermissionsMixin  # PermissionsMixin 임포트
from django.db import models  # Django 모델 임포트

from .validator import validate_password  # 비밀번호 유효성 검사 임포트

# 전방 참조를 위한 타입 변수 선언 (CustomUser를 상속하는 타입을 지정)
CustomUserType = TypeVar("CustomUserType", bound="CustomUser")


class CustomUserManager(BaseUserManager[CustomUserType]):  # BaseUserManager에 제네릭 타입 파라미터 추가
    def create_user(self, email: str, password: Optional[str] = None, **extra_fields: Any) -> CustomUserType:
        # 이메일이 제공되지 않은 경우 예외 발생
        if not email:
            raise ValueError("이메일은 필수 입력사항입니다.")
        # 이메일 정규화
        email = self.normalize_email(email)
        # 사용자 인스턴스 생성 (모델의 전방 참조 사용)
        user: CustomUserType = self.model(email=email, **extra_fields)
        # 비밀번호 검사 후 저장
        if password:
            validate_password(password)  # type: ignore
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields: Any) -> CustomUserType:
        # 일반 사용자 생성 후 슈퍼유저 플래그 설정
        user = self.create_user(email, password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("이메일", max_length=20, unique=True)
    nickname = models.CharField("닉네임", max_length=20)
    name = models.CharField("이름", max_length=10)
    phone_number = models.CharField("전화번호", max_length=20, unique=True)
    last_login = models.DateTimeField("마지막 로그인", auto_now_add=True)
    is_staff = models.BooleanField("스태프 여부", default=False)
    is_admin = models.BooleanField("관리자 여부", default=False)
    is_active = models.BooleanField("활성 여부", default=False)

    objects = CustomUserManager()  # 사용자 매니저 설정

    USERNAME_FIELD = "email"  # 기본 로그인 시 이메일 사용
    REQUIRED_FIELDS = [
        "nickname",
        "name",
        "phone_number",
    ]  # 필수 필드 지정

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자 목록"

    def __str__(self) -> str:
        return self.email


class Account(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="accounts",
        verbose_name="유저 정보",
    )
    account_number = models.CharField("계좌번호", max_length=30, unique=True)
    bank_code = models.CharField("은행 코드", max_length=20)
    account_type = models.CharField("계좌 종류", max_length=20)
    balance = models.DecimalField("잔액", max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = "계좌"
        verbose_name_plural = "계좌 목록"

    def __str__(self) -> str:
        return f"{self.account_type} - {self.account_number}"


class TransactionHistory(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="계좌 정보",
    )
    transaction_amount = models.DecimalField("거래 금액", max_digits=15, decimal_places=2)
    after_balance = models.DecimalField("잔액", max_digits=15, decimal_places=2)
    transaction_detail = models.CharField("계좌 인자 내역", max_length=30)
    deposit_withdrawal_type = models.CharField("입출금 타입", max_length=10)
    transaction_type = models.CharField("거래 타입", max_length=10)
    transaction_date = models.DateTimeField("거래 일시", auto_now_add=True)

    class Meta:
        verbose_name = "거래 내역"
        verbose_name_plural = "거래 내역 목록"

    def save(self, *args: Any, **kwargs: Any) -> None:
        # 거래 타입(입금/출금)에 따라 계좌의 잔액을 계산합니다.
        # deposit_withdrawal_type 필드의 값에 따라 분기합니다.
        if self.deposit_withdrawal_type.lower() in "입금":
            # 입금인 경우, 현재 계좌 잔액에 거래 금액을 더하여 후 잔액 계산
            self.after_balance = self.account.balance + self.transaction_amount  # 계산된 후 잔액
        elif self.deposit_withdrawal_type.lower() in "출금":
            # 출금인 경우, 현재 계좌 잔액에서 거래 금액을 빼서 후 잔액 계산
            self.after_balance = self.account.balance - self.transaction_amount  # 계산된 후 잔액
        else:
            # 거래 타입이 명시되지 않은 경우, 기존 잔액 유지 (기본값)
            self.after_balance = self.account.balance

        # 거래 내역이 저장되기 전에, 해당 계좌의 잔액을 거래 후 잔액으로 업데이트
        self.account.balance = self.after_balance
        # 계좌 모델의 변경 사항을 먼저 저장
        self.account.save()

        # 이후, TransactionHistory 모델의 인스턴스를 저장
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.deposit_withdrawal_type} - {self.transaction_amount} - {self.after_balance}"
