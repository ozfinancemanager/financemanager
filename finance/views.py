from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account

# 사용자가 본인 계좌를 삭제할 수 있게 해주는 API

class AccountDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, account_id):
        # 요청된 account_id에 해당하는 계좌 가져오기
        account = get_object_or_404(Account, id=account_id, user=request.user)

        # 계좌 삭제 수행
        account.delete()

        return Response({"message": "계좌가 정상적으로 삭제되었습니다."}, status=status.HTTP_200_OK)
