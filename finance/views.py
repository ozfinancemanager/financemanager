from decimal import Decimal

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account, TransactionHistory
from .serializers import TransactionHistorySerializer

from .serializers import AccountSerializer


# CBV로 작성
# 거래내역 목록 조회 및 생성 API (APIView 썼습니다)
class TransactionHistoryListCreate(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능 / 이거 기능 되는지 안되는지 확인해보세요

    def get(self, request):
        # 현재 사용자의 계좌 목록 가져오기
        user_accounts = Account.objects.filter(user=request.user).values_list("id", flat=True)  # 계좌 ID만 가져오기

        # 사용자 계좌의 거래내역만 필터링
        transactions = TransactionHistory.objects.filter(account__in=user_accounts)  # 계좌 ID로 필터링

        # 필터링 옵션 처리
        account_id = request.query_params.get("account")  # 계좌 ID
        deposit_withdrawal_type = request.query_params.get("deposit_withdrawal_type")  # 입출금 타입
        transaction_type = request.query_params.get("transaction_type")  # 거래 타입
        min_amount = request.query_params.get("min_amount")  # 최소 금액
        max_amount = request.query_params.get("max_amount")  # 최대 금액

        # 계좌별 필터링
        if account_id:
            transactions = transactions.filter(account_id=account_id)

        # 입출금 타입 필터링
        if deposit_withdrawal_type:
            transactions = transactions.filter(deposit_withdrawal_type=deposit_withdrawal_type)

        # 거래 타입 필터링
        if transaction_type:
            transactions = transactions.filter(transaction_type=transaction_type)

        # 최소 금액 필터링
        if min_amount:
            transactions = transactions.filter(transaction_amount__gte=Decimal(min_amount))

        # 최대 금액 필터링
        if max_amount:
            transactions = transactions.filter(transaction_amount__lte=Decimal(max_amount))

        # 정렬 (최신순)
        transactions = transactions.order_by("-transaction_date")

        # 직렬화 및 응답
        serializer = TransactionHistorySerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        새 거래 내역 생성

        요청 데이터:
        - account: 계좌 ID
        - transaction_amount: 거래 금액
        - transaction_detail: 거래 내역 설명
        - deposit_withdrawal_type: 입금/출금 구분
        - transaction_type: 거래 유형
        """
        data = request.data.copy()
        account_id = data.get("account")
        deposit_withdrawal_type = data.get("deposit_withdrawal_type")
        transaction_amount = Decimal(data.get("transaction_amount", 0))

        # 계좌가 사용자의 것인지 확인
        try:
            account = Account.objects.get(id=account_id, user=request.user)
        except Account.DoesNotExist:
            return Response(
                {"error": "존재하지 않는 계좌이거나 접근 권한이 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )

        # 출금 시 잔액 충분한지 확인
        if deposit_withdrawal_type.upper() == "출금" and account.balance < transaction_amount:
            return Response({"error": "잔액이 부족합니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 거래내역 저장 (TransactionHistory 모델의 save 메서드에서 계좌 잔액 자동 업데이트)
        serializer = TransactionHistorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 거래내역 상세 조회, 수정, 삭제 API (요것도 APIView 썼습니다)
class TransactionHistoryDetail(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get_object(self, pk, user):
        # 사용자의 계좌 목록 가져오기
        user_accounts = Account.objects.filter(user=user).values_list("id", flat=True)
        # 해당 거래내역이 사용자의 계좌에 속하는지 확인하며 가져오기
        return get_object_or_404(TransactionHistory, id=pk, account__in=user_accounts)

    def get(self, request, pk):
        """특정 거래 내역 조회"""
        transaction = self.get_object(pk, request.user)
        serializer = TransactionHistorySerializer(transaction)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        거래 내역 수정

        기존 거래 취소 후 새 거래 적용
        """
        transaction = self.get_object(pk, request.user)
        account = transaction.account

        # 기존 거래내역 정보 저장
        old_deposit_withdrawal_type = transaction.deposit_withdrawal_type
        old_amount = transaction.transaction_amount

        # 새로운 거래내역 정보
        data = request.data.copy()
        new_deposit_withdrawal_type = data.get("deposit_withdrawal_type", old_deposit_withdrawal_type)
        new_amount = Decimal(data.get("transaction_amount", old_amount))

        # 기존 거래 취소하여 잔액 되돌리기
        if old_deposit_withdrawal_type.upper() == "입금":
            account.balance -= old_amount
        elif old_deposit_withdrawal_type.upper() == "출금":
            account.balance += old_amount

        # 출금 시 잔액 확인
        if new_deposit_withdrawal_type.upper() == "출금" and account.balance < new_amount:
            # 잔액 부족 시 원상복구
            if old_deposit_withdrawal_type.upper() == "입금":
                account.balance += old_amount
            elif old_deposit_withdrawal_type.upper() == "출금":
                account.balance -= old_amount
            account.save()

            return Response({"error": "잔액이 부족합니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 직렬화 및 저장 (모델의 save 메서드에서 새 거래 적용)
        serializer = TransactionHistorySerializer(transaction, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        # 유효성 검증 실패 시 원상복구
        if old_deposit_withdrawal_type.upper() == "입금":
            account.balance += old_amount
        elif old_deposit_withdrawal_type.upper() == "출금":
            account.balance -= old_amount
        account.save()

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        거래 내역 부분 수정

        put 메서드와 동일하게 처리 (전체 수정과 동일)
        """
        return self.put(request, pk)

    def delete(self, request, pk):
        """
        거래 내역 삭제

        거래 취소 효과 적용 및 거래내역 삭제
        """
        transaction = self.get_object(pk, request.user)
        account = transaction.account

        # 거래 취소 효과 적용
        if transaction.deposit_withdrawal_type.upper() == "입금":
            account.balance -= transaction.transaction_amount
        elif transaction.deposit_withdrawal_type.upper() == "출금":
            account.balance += transaction.transaction_amount
        account.save()

        # 거래내역 삭제
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
