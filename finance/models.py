from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from .validator import validate_password


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email: raise ValueError('이메일은 필수 입력사항입니다.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            validate_password(password)
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('이메일', max_length=20, unique=True)
    nickname = models.CharField('닉네임', max_length=20)
    name = models.CharField('이름', max_length=5)
    phone_number = models.CharField('전화번호', max_length=20, unique=True)
    last_login = models.DateTimeField('마지막 로그인', auto_now=True)
    is_staff = models.BooleanField('스태프 여부', default=False)
    is_admin = models.BooleanField('관리자 여부', default=False)
    is_active = models.BooleanField('활성 여부', default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email' # 기본 로그인시 이메일로 로그인
    REQUIRED_FIELDS = ['nickname', 'name', 'phone_number'] # 이메일, 닉네임, 이름, 전화번호 필수

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자 목록'
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.email


class Account(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='accounts', verbose_name='유저 정보')
    account_number = models.CharField('계좌번호', max_length=30, unique=True)
    bank_code = models.CharField('은행 코드', max_length=20)
    account_type = models.CharField('계좌 종류', max_length=20)
    balance = models.DecimalField('잔액', max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = '계좌'
        verbose_name_plural = '계좌 목록'

    def __str__(self):
        return f"{self.bank_code} - {self.account_number}"

class TransactionHistory(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions', verbose_name='계좌 정보')
    transaction_amount = models.DecimalField('거래 금액', max_digits=15, decimal_places=2)
    after_balance = models.DecimalField('거래 후 잔액', max_digits=15, decimal_places=2)
    transaction_detail = models.CharField('계좌 인자 내역', max_length=30)
    deposit_withdrawal_type = models.CharField('입출금 타입', max_length=10)
    transaction_type = models.CharField('거래 타입', max_length=5)
    transaction_date = models.DateTimeField('거래 일시', auto_now_add=True)

    class Meta:
        verbose_name = '거래 내역'
        verbose_name_plural = '거래 내역 목록'


    def __str__(self):
        return f"{self.deposit_withdrawal_type} - {self.transaction_amount} - {self.after_balance}"







