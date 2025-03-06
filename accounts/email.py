from django.conf import settings
from django.core.mail import send_mail
from django.core.signing import TimestampSigner

# TimestampSigner 생성
signer = TimestampSigner()  # 데이터에 서명하고 검증하는 역할 (유효기간 설정, 위변조 방지)


def generate_email_verification_token(user):  # 이메일 토큰 생성 함수
    token = signer.sign(user.pk)  # 사용자 pk를 서명하여 토큰 생성
    return token  # 토큰 반환


def send_verification_email(user):  # 이메일 전송 함수
    token = generate_email_verification_token(user)  # 사용자 인증 토큰 생성
    verification_link = f"{settings.SITE_URL}/verify-email/?token={token}"  # settings에 SITE_URL(나중에 도메인)을 불러와 이메일 인증 링크 생성
    subject = "이메일 인증 요청"  # 이메일 제목
    # 대체 텍스트 메세지
    message = f"저희 Finance Manager에 회원가입을 진심으로 환영합니다. 아래 링크를 클릭하여 이메일 인증을 완료해주세요\n{verification_link}"
    from_email = settings.DEFAULT_FROM_EMAIL  # 발신자 이메일 주소
    recipient_list = [user.email]  # 수신자

    # HTML 템플릿에 사용할 변수들(이쁘게)
    point_color = "#02b875"  # 색
    site_title_top = "Register"  # 부제
    site_title_content = "Finance Manager"  # 제목
    auth_url = verification_link  # 인증링크

    # HTML 형식의 메시지 구성 (클릭 가능한 링크 포함)
    html_message = f"""<div style="font-family: 'Apple SD Gothic Neo', 'sans-serif' !important; width: 540px; height: 600px; border-top: 4px solid {point_color}; margin: 100px auto; padding: 30px 0; box-sizing: border-box;">
            <h1 style="margin: 0; padding: 0 5px; font-size: 28px; font-weight: 400;">
                <span style="font-size: 15px; margin: 0 0 10px 3px;">{site_title_top}</span><br />
                <span style="color: {point_color};">메일인증</span> 안내입니다.
            </h1>
            <p style="font-size: 16px; line-height: 26px; margin-top: 50px; padding: 0 5px;">
                안녕하세요.<br />
                {site_title_content}에 가입해 주셔서 진심으로 감사드립니다.<br />
                아래 <b style="color: {point_color};">'메일 인증'</b> 버튼을 클릭하여 회원가입을 완료해 주세요.<br />
                감사합니다.
            </p>
            <a style="color: #FFF; text-decoration: none; text-align: center;" href="{auth_url}" target="_blank">
                <p style="display: inline-block; width: 210px; height: 45px; margin: 30px 5px 40px; background: {point_color}; line-height: 45px; vertical-align: middle; font-size: 16px;">메일 인증</p>
            </a>
            <div style="border-top: 1px solid #DDD; padding: 5px;">
                <p style="font-size: 13px; line-height: 21px; color: #555;">
                    만약 버튼이 정상적으로 클릭되지 않는다면, 아래 링크를 복사하여 접속해 주세요.<br />
                    {auth_url}
                </p>
            </div>
        </div>"""

    # HTML 메시지를 포함하여 이메일 전송 (fail_silently=False로 오류 발생 시 예외 처리)
    send_mail(subject, message, from_email, recipient_list, html_message=html_message, fail_silently=False)
