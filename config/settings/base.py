"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.25.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-8a9shn#cj6c1_*lg5c6!m%-91*us_5qu1-c4u=ppxgye*k)11g"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS: list[str] = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",
    "finance",
    "core",
    "accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls.urls_dev"  # 개발환경 urls.dev 사용중

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "djangomini",
        "USER": "postgres",
        "PASSWORD": "1234",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

AUTH_USER_MODEL = "finance.CustomUser"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "ko-KR"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
}

SIMPLE_JWT = {  # 심플 JWT 세팅
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),  # 액세스토큰 시간
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),  # 리프레시토큰 시간
    "ROTATE_REFRESH_TOKENS": False,
    # refresh 토큰 재발급 여부 설정  -> True 설정시 refrsh token 제출 시 새 엑세스 토큰 + 새 리프레쉬 토큰 반환
    "BLACKLIST_AFTER_ROTATION": True,  # 토큰 사용 후 블랙리스트 적용
    # 사용된 리프레쉬 토큰 블랙리스트 추가
    "AUTH_HEADER_TYPES": ("Bearer",),  # 인증 헤더에 사용할 토큰 타입 지정
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 이메일 백엔드 (개발 콘솔용) *수정 필요

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"  # SMTP 백엔드 사용
EMAIL_HOST = "smtp.naver.com"  # 네이버 SMTP 서버
EMAIL_PORT = 465
EMAIL_USE_SSL = True
# os.environ.get -> 환경변수에서 값을 우선 가져온 후 없으면 뒤에 있는 값
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "ebiella@naver.com")  # 네이버 아이디@naver.com
EMAIL_HOST_PASSWORD = os.environ.get(
    "EMAIL_HOST_PASSWORD", "*********"
)  # 네이버 비밀번호  -> 깃허브 시크릿 EMAIL_HOST_PASSWORD / 비밀번호 세팅
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "ebiella@naver.com")  # 기본 발신자 이메일 주소
SITE_URL = "http://localhost:8000"  # 나중에 도메인으로 변경
