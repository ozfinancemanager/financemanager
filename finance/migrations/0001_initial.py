import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("email", models.EmailField(max_length=20, unique=True, verbose_name="이메일")),
                ("nickname", models.CharField(max_length=20, verbose_name="닉네임")),
                ("name", models.CharField(max_length=10, verbose_name="이름")),
                ("phone_number", models.CharField(max_length=20, unique=True, verbose_name="전화번호")),
                ("last_login", models.DateTimeField(auto_now_add=True, verbose_name="마지막 로그인")),
                ("is_staff", models.BooleanField(default=False, verbose_name="스태프 여부")),
                ("is_admin", models.BooleanField(default=False, verbose_name="관리자 여부")),
                ("is_active", models.BooleanField(default=False, verbose_name="활성 여부")),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "사용자",
                "verbose_name_plural": "사용자 목록",
            },
        ),
        migrations.CreateModel(
            name="Account",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("account_number", models.CharField(max_length=30, unique=True, verbose_name="계좌번호")),
                ("bank_code", models.CharField(max_length=20, verbose_name="은행 코드")),
                ("account_type", models.CharField(max_length=20, verbose_name="계좌 종류")),
                ("balance", models.DecimalField(decimal_places=2, max_digits=15, verbose_name="잔액")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="accounts",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="유저 정보",
                    ),
                ),
            ],
            options={
                "verbose_name": "계좌",
                "verbose_name_plural": "계좌 목록",
            },
        ),
        migrations.CreateModel(
            name="TransactionHistory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("transaction_amount", models.DecimalField(decimal_places=2, max_digits=15, verbose_name="거래 금액")),
                ("after_balance", models.DecimalField(decimal_places=2, max_digits=15, verbose_name="잔액")),
                ("transaction_detail", models.CharField(max_length=30, verbose_name="계좌 인자 내역")),
                ("deposit_withdrawal_type", models.CharField(max_length=10, verbose_name="입출금 타입")),
                ("transaction_type", models.CharField(max_length=10, verbose_name="거래 타입")),
                ("transaction_date", models.DateTimeField(auto_now_add=True, verbose_name="거래 일시")),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions",
                        to="finance.account",
                        verbose_name="계좌 정보",
                    ),
                ),
            ],
            options={
                "verbose_name": "거래 내역",
                "verbose_name_plural": "거래 내역 목록",
            },
        ),
        migrations.CreateModel(
            name="notifications",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("message", models.TextField(verbose_name="메세지 내용")),
                ("is_read", models.BooleanField(default=False, verbose_name="읽음 여부")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="생성일")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notifications",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="notifications",
                    ),
                ),
            ],
            options={
                "verbose_name": "알림",
                "verbose_name_plural": "알림 목록",
            },
        ),
        migrations.CreateModel(
            name="Analysis",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "target",
                    models.CharField(
                        choices=[("수입", "수입"), ("지출", "지출")], max_length=10, verbose_name="분석 대상"
                    ),
                ),
                (
                    "period",
                    models.CharField(
                        choices=[("일간", "일간"), ("주간", "주간"), ("월간", "월간"), ("연간", "연간")],
                        max_length=10,
                        verbose_name="분석 기간",
                    ),
                ),
                ("start_date", models.DateField(verbose_name="시작 날짜")),
                ("end_date", models.DateField(verbose_name="종료 날짜")),
                ("description", models.TextField(blank=True, null=True, verbose_name="설명")),
                (
                    "result_image",
                    models.ImageField(blank=True, null=True, upload_to="analysis_images/", verbose_name="결과 이미지"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="생성일")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="수정일")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="analysis",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="analysis",
                    ),
                ),
            ],
            options={
                "verbose_name": "분석",
                "verbose_name_plural": "분석 목록",
            },
        ),
    ]