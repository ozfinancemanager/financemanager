# views.py
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from config import settings

from .models import CustomUser

# Create your views here.


def signup_view(request): # type: ignore
    # 회원가입 처리 뷰 POST
    # is_active=FALSE로 생성하고, 인증 이메일 발송
    if request.method == "POST":
        email = request.POST.get("이메일")
        password = request.POST.get("비밀번호")
        nickname = request.POST.get("닉네임")
        name = request.POST.get("이름")
        phone_number = request.POST.get("전화번호")

        # 사용자 생성
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            nickname=nickname,
            name=name,
            phone_number=phone_number,
            is_active=False,
        )

    # 토큰 생성
    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

    # 인증 링크 생성 (예: http://example.com/verify/<uidb64>/<token>/ )
    verify_url = request.build_absolute_uri(reverse("verify_email", kwargs={"uidb64": uidb64, "token": token}))

    # 4) 이메일 발송
    send_mail(
        subject="회원가입 인증을 완료해주세요",
        message=f"아래 링크를 클릭하여 인증을 완료하세요:\n{verify_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,  # settings.py에서 설정
        recipient_list=[email],
        fail_silently=False,
    )

    # return render(request, "템플릿 집어넣기")

    # return render(request, "템플릿 집어넣기")


# 인증 부분은 거의 코드 복붙이라서 오류 있으시면 꼭 알려주십쇼
# 여러분의 도움이 필요합니다
# 구글링 + gpt의 도움으로 작성한겁니다
def verify_email_view(request, uidb64, token): # type: ignore
    # 이메일 인증 링크를 통해 계정을 활성화하는 뷰
    # URL로부터 uidb64, token을 받아 유효성 검증
    # 검증 성공 시 user.is_active=True로 업데이트

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # 템플릿 리턴
        # return render(request, "템플릿 넣기")
    # else:
    # return render(request, "템플릿 넣기")
