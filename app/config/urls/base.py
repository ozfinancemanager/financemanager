"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from app.accounts.views import (
    LoginAPIView,
    LogoutAPIView,
    RegisterAPIView,
    UserProfileAPIView,
    VerifyEmailAPIView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", RegisterAPIView.as_view(), name="register"),  # 회원가입 URL 패턴
    path("login/", LoginAPIView.as_view(), name="login"),  # 로그인 URL 패턴
    path("logout/", LogoutAPIView.as_view(), name="logout"),  # 로그아웃 URL 패턴
    path("verify-email/", VerifyEmailAPIView.as_view(), name="verify-email"),  # 이메일 인증 URL 패턴
    path(
        "profile/", UserProfileAPIView.as_view(), name="user-profile"
    ),  # 인증된 사용자가 자신의 프로필을 확인, 수정, 삭제할 수 있는 URL 등록
    path("api/", include("finance.urls")),
]
