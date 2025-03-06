# from django.contrib.auth import get_user_model  # 현재 프로젝트에서 사용하는 사용자 모델 가져오기
# from django.core.signing import TimestampSigner  # 이메일 인증 토큰 생성 및 검증을 위해 사용
# from django.urls import reverse  # URL을 이름으로 역방향 조회하기 위해 reverse 함수 사용
# from rest_framework import status  # HTTP 상태 코드를 비교하기 위해 사용
# from rest_framework.test import APITestCase  # DRF에서 제공하는 테스트 케이스 클래스
#
# User = get_user_model()  # 프로젝트에서 사용하는 User 모델을 변수에 저장
#
#
# class UserAPITest(APITestCase):
#
#     def setUp(self):
#         self.register_url = reverse("register")  # 예: path('register/', RegisterAPIView.as_view(), name='register')
#         self.verify_url = reverse(
#             "verify-email"
#         )  # 예: path('verify-email/', VerifyEmailAPIView.as_view(), name='verify-email')
#         self.login_url = reverse("login")  # 예: path('login/', LoginAPIView.as_view(), name='login')
#         self.logout_url = reverse("logout")  # 예: path('logout/', LogoutAPIView.as_view(), name='logout')
#         self.profile_url = reverse(
#             "user-profile"
#         )  # 예: path('profile/', UserProfileAPIView.as_view(), name='user-profile')
#
#         self.test_email = "testuser@example.com"  # 회원가입에 사용할 테스트 이메일
#         self.test_password = "testpassword123"  # 회원가입에 사용할 테스트 비밀번호
#         self.test_nickname = "testnickname"
#         self.test_name = "testname"
#         self.test_phone_number = "010101010101010"
#
#     def test_user_registration_and_email_verification(self):
#         # 회원가입 API 테스트
#         register_data = {
#             "email": self.test_email,
#             "password": self.test_password,
#             "nickname": self.test_nickname,
#             "name": self.test_name,
#             "phone_number": self.test_phone_number,
#         }
#         response = self.client.post(self.register_url, register_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#         # 회원가입 후 사용자가 DB에 생성되었는지 확인
#         user = User.objects.get(email=self.test_email)
#         self.assertFalse(user.is_active)
#
#         # 이메일 인증 VerifyEmailAPI 테스트
#         signer = TimestampSigner()
#         token = signer.sign(user.pk)  # user.pk를 서명된 문자열로 반환
#
#         # 인증 URL(GET 요청)에 token 파라미터를 붙여 전송
#         # 예: reverse("verify-email") == "/verify-email/" 라면, 실제 요청은 "/verify-email/?token=..."
#         verify_url_with_token = f"{self.verify_url}?token={token}"
#         response = self.client.get(verify_url_with_token)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)  # 상태코드 같은 지 비교
#
#         user.refresh_from_db()  # 데이터베이스에서 사용자 가져와서
#         self.assertTrue(user.is_active)  # is_active가 True인지 비교
#
#     def test_user_login_and_logout(self):
#         # 우선 테스트용 사용자 계정을 만들어 둡니다(이미 이메일 인증된 상태로 가정).
#         user = User.objects.create_user(
#             email=self.test_email, password=self.test_password, is_active=True  # 이메일 인증 완료 상태로 가정
#         )
#
#         # 로그인 LoginAPI테스트
#         # -------------------------------------------------
#         login_data = {
#             "email": self.test_email,  # LoginSerializer/뷰 로직에 따라 username이 필요할 수도 있음
#             "password": self.test_password,
#         }
#         response = self.client.post(self.login_url, login_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         # 발급된 JWT 토큰(access, refresh)가 정상적으로 응답 데이터에 있는지 확인
#         self.assertIn("access", response.data)
#         self.assertIn("refresh", response.data)
#
#         refresh_token = response.data["refresh"]  # 로그아웃 시 필요한 refresh 토큰
#
#         # 로그아웃 LogoutAPI 테스트
#         # -------------------------------------------------
#         logout_data = {"refresh": refresh_token}
#         response = self.client.post(self.logout_url, logout_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
#
#     def test_user_profile_crud(self):
#         # 우선 테스트용 사용자 계정을 만들어 둡니다(이메일 인증 완료로 가정).
#         user = User.objects.create_user(email=self.test_email, password=self.test_password, is_active=True)
#
#         # 토큰 발급(로그인) 후 헤더에 access 토큰을 설정하여 인증이 필요한 요청을 수행해야 합니다.
#         login_data = {"email": self.test_email, "password": self.test_password}
#         response = self.client.post(self.login_url, login_data, format="json")
#         access_token = response.data["access"]  # 발급받은 Access 토큰
#
#         # 이후 요청은 헤더에 인증 토큰이 있어야 하므로, client.credentials()를 사용합니다.
#         self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
#
#         # 프로필 조회
#         # -------------------------------------------------
#         response = self.client.get(self.profile_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn("email", response.data)
#         self.assertEqual(response.data["email"], self.test_email)
#
#         # 프로필 수정
#         # -------------------------------------------------
#         update_data = {"nickname": "NewNickName"}  # 실제 ProfileSerializer에서 허용하는 필드를 사용해야 함
#         response = self.client.patch(self.profile_url, update_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data.get("nickname"), "NewNickName")
#
#         # 3) 회원탈퇴 (DELETE)
#         # -------------------------------------------------
#         response = self.client.delete(self.profile_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         # 탈퇴 후 해당 계정이 실제로 삭제되었는지 확인
#         with self.assertRaises(User.DoesNotExist):
#             User.objects.get(email=self.test_email)
