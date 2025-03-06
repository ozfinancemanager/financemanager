from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from finance.models import Account
from finance.serializers import AccountSerializer


# Account생성 API
class AccountListCreateView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만

    # 전체조회 API
    def get(self, request):
        account = Account.objects.filter(user=request.user)  # user에 연결된 Account만 조회
        serializer = AccountSerializer(account, many=True)  # Account를 직렬화 many-> 여러개
        return Response(serializer.data, status=status.HTTP_200_OK)  # 데이터, 상태코드 반환

    # 생성 API
    def post(self, request):
        print("DEBUG: request.user =", request.user)
        print("DEBUG: request.user.id =", request.user.id)
        data = request.data.copy()  # data를 복사
        data["user"] = request.user.id  # user.id를 data에 user에 넣음
        serializer = AccountSerializer(data=data)  # 직렬화 데이터 전달

        if serializer.is_valid():
            print("DEBUG validated_data:", serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # 데이터, 상태코드 반환
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 데이터, 상태코드 반환


# 특정 계좌 조회 API
class AccountDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만

    # user의 pk 계좌
    def get_object(self, user, pk):
        try:
            return Account.objects.get(pk=pk, user=user)  # user에 pk 계좌를 가져옴
        except Account.DoesNotExist:  # 없으면 None 반환
            return None

    # 단일 계좌 정보 조회
    def get(self, request, pk):
        account = self.get_object(request.user, pk)  # get_object 사용해 계좌 가져옴
        if not account:  # account가
            return Response({"detail": "계좌를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AccountSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)
