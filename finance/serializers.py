from rest_framework import serializers

from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):  # type: ignore
    # 클라이언트로부터 비밀번호를 입력받음
    # write_only로 처리하여 응답에 포함x
    password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})


class Meta:
    model = CustomUser
    # 회원가입 시 필요한 필드: 이메일, 전화번호, 비밀번호, 닉네임, 이름
    fields = ("email", "phone_number", "password", "nickname", "name")

    # cumtomuser 매니저 create_user()호출
    # set_password() 사용 => 비밀번호 암호화


def create(self, validated_data):  # type: ignore
    user = CustomUser.objects.create_user(**validated_data)
    return user
