# Generated by Django 4.2.19 on 2025-03-06 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finance", "0002_alter_account_account_type_alter_account_bank_code_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="email",
            field=models.EmailField(max_length=50, unique=True, verbose_name="이메일"),
        ),
    ]
