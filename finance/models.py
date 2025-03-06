from typing import Any, Optional, TypeVar

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.password_validation import validate_password
from django.db import models

# constants.py에서 상수들을 import
from .constants import (
    ACCOUNT_TYPE,
    ANALYSIS_TYPES,
    BANK_CODES,
    TRANSACTION_METHOD,
    TRANSACTION_TYPE,
)

# 전방 참조를 위한 타입 변수 선언 (CustomUser를 상속하는 타입 지정)
CustomUserType = TypeVar("CustomUserType", bound="CustomUser")


class CustomUserManager(BaseUserManager[CustomUserType]):
    def create_user(self, email: str, password: Optional[str] = None, **extra_fields: Any) -> CustomUserType:
        if not email:
            raise ValueError("이메일은 필수 입력사항입니다.")
        email = self.normalize_email(email)
        user: CustomUserType = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields: Any) -> CustomUserType:
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
    is_staff = models.BooleanField("스태프 여부", default=False)
    is_admin = models.BooleanField("관리자 여부", default=False)
    is_active = models.BooleanField("활성 여부", default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname", "name", "phone_number"]

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
    bank_code = models.CharField("은행 코드", max_length=20, choices=BANK_CODES)
    account_type = models.CharField("계좌 종류", max_length=20, choices=ACCOUNT_TYPE)
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
    deposit_withdrawal_type = models.CharField("입출금 타입", max_length=10, choices=TRANSACTION_TYPE)
    transaction_type = models.CharField("거래 타입", max_length=20, choices=TRANSACTION_METHOD)
    transaction_date = models.DateTimeField("거래 일시", auto_now_add=True)

    class Meta:
        verbose_name = "거래 내역"
        verbose_name_plural = "거래 내역 목록"

    def save(self, *args: Any, **kwargs: Any) -> None:
        # deposit_withdrawal_type에는 "DEPOSIT" 또는 "WITHDRAW"가 저장됩니다.
        if self.deposit_withdrawal_type.upper() == "입금":
            self.after_balance = self.account.balance + self.transaction_amount
        elif self.deposit_withdrawal_type.upper() == "출금":
            self.after_balance = self.account.balance - self.transaction_amount
        else:
            self.after_balance = self.account.balance

        self.account.balance = self.after_balance
        self.account.save()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.deposit_withdrawal_type} - {self.transaction_amount} - {self.after_balance}"


class Analysis(models.Model):
    INCOME = "수입"
    EXPENSE = "지출"
    TARGET_CHOICES = [
        (INCOME, "수입"),
        (EXPENSE, "지출"),
    ]

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="analysis", verbose_name="분석 요청 사용자"
    )
    target = models.CharField("분석 대상", max_length=10, choices=TARGET_CHOICES)
    period = models.CharField("분석 기간", max_length=10, choices=ANALYSIS_TYPES)
    start_date = models.DateField("시작 날짜")
    end_date = models.DateField("종료 날짜")
    description = models.TextField("설명", blank=True, null=True)
    result_image = models.ImageField("결과 이미지", upload_to="analysis_images/", blank=True, null=True)
    created_at = models.DateTimeField("생성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        verbose_name = "분석"
        verbose_name_plural = "분석 목록"

    def __str__(self) -> str:
        return f"{self.user} - {self.target} - {self.period} {self.start_date} ~ {self.end_date}"


class notifications(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="알림 수신 사용자",
    )
    message = models.TextField("메세지 내용")
    is_read = models.BooleanField("읽음 여부", default=False)
    created_at = models.DateTimeField("생성일", auto_now_add=True)

    class Meta:
        verbose_name = "알림"
        verbose_name_plural = "알림 목록"

    def __str__(self) -> str:
        status = "읽음" if self.is_read else "안읽음"
        return f"{self.user} - {self.message} - {status}"
