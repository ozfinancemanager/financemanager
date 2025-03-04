from django.contrib import admin  # Django의 관리자(admin) 관련 모듈 import

from finance.models import Account, CustomUser, TransactionHistory  # 모델 import


# CustomUser 모델에 대한 관리자 설정
class CustomUserAdmin(admin.ModelAdmin):  # type: ignore
    # 페이지에 표시할 필드들 설정
    list_display = ("email", "nickname", "name", "phone_number")
    # 하이퍼링크 설정
    list_display_links = ["email", "nickname", "name", "phone_number"]
    # 닉네임으로 검색가능
    search_fields = ("nickname",)

    # 관리자 상세 페이지에서 보여줄 필드 구분(Fieldsets) 설정
    fieldsets = (
        (
            "기본 정보",
            {
                "fields": ("email", "password"),
            },
        ),
        (
            "개인 정보",
            {
                "fields": ("nickname", "name", "phone_number"),
            },
        ),
        (
            "권한",
            {
                "fields": ("is_active", "is_staff", "is_admin", "is_superuser"),
            },
        ),
    )
    # 사용자 생성 시 추가 필드 설정
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),  # CSS 클래스 지정 (wide: 넓은 폼)
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "nickname",
                    "name",
                    "phone_number",
                ),  # 생성 시 필요한 필드들
            },
        ),
    )


# Account 모델에 대한 관리자 설정
class CustomAccount(admin.ModelAdmin[Account]):
    # 페이지에 표시할 필드들 설정
    list_display = ("account_number", "bank_code", "account_type", "balance")
    # 하이퍼링크 설정
    list_display_links = ("account_number", "bank_code", "account_type", "balance")
    # 계좌번호 또는 은행코드로 검색 가능
    search_fields = ("account_number", "bank_code")

    fieldsets = (
        (
            "사용자",
            {
                "fields": ("user",),
            },
        ),
        (
            "계좌 정보",
            {
                "fields": ("bank_code", "account_type", "account_number"),
            },
        ),
        (
            "잔액",
            {
                "fields": ("balance",),
            },
        ),
    )


# TransactionHistory 모델에 대한 관리자 설정
class CustomTransaction(admin.ModelAdmin[TransactionHistory]):
    # 페이지에 표시할 필드들 설정
    list_display = ("account", "transaction_amount", "after_balance")
    # 계좌번호로 검색가능
    search_fields = ("account__account_number",)

    fieldsets = (
        (
            "계좌 정보",
            {
                "fields": ("account", "transaction_amount", "after_balance"),
            },
        ),
        (
            "거래 상세 정보",
            {
                "fields": ("transaction_detail", "deposit_withdrawal_type", "transaction_type"),
            },
        ),
        (
            "거래 일시",
            {
                "fields": ("transaction_date",),  # 거래 발생 일시
            },
        ),
    )
    readonly_fields = ("transaction_date",)  # 읽기 전용


# 관리자 사이트에 모델과 관리자 설정 등록
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Account, CustomAccount)
admin.site.register(TransactionHistory, CustomTransaction)
