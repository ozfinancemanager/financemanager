# core/management/commands/wait_for_db.py
# 이 파일은 Django의 커스텀 관리 명령어를 정의하는 모듈입니다.
# 이 명령어는 데이터베이스가 준비될 때까지 연결을 시도하여, 준비되면 성공 메시지를,
# 10번의 시도 후에도 연결되지 않으면 실패 메시지를 출력합니다.

import time  # 재시도 시 딜레이를 주기 위한 모듈 임포트
from typing import Any

from django.core.management.base import BaseCommand  # 커스텀 명령어 생성을 위한 BaseCommand 상속
from django.db import connections  # Django에서 설정한 데이터베이스 연결 객체를 가져오기 위함
from django.db.utils import OperationalError  # Django에서 발생하는 OperationalError 예외 처리
from psycopg2 import OperationalError as Psycopg2OpError  # psycopg2에서 발생하는 예외 처리


class Command(BaseCommand):
    # 커맨드에 대한 도움말 메시지를 지정합니다.
    help = "Django command to wait for the database to be available"

    def handle(self, *args: Any, **options: Any) -> None:
        # 최대 10번까지 데이터베이스 연결을 시도합니다.
        for i in range(10):
            # 현재 시도 횟수와 함께 데이터베이스 대기 메시지를 출력합니다.
            self.stdout.write(f"Try {i+1}: Waiting for database...")
            try:
                # 기본 데이터베이스 연결 객체를 가져옵니다.
                connection = connections["default"]
                # 연결이 성공적으로 설정되었는지 확인합니다.
                if connection:
                    # 연결에 성공했다면 성공 메시지를 출력하고 커맨드를 종료합니다.
                    self.stdout.write(self.style.SUCCESS("PostgreSQL Database available!"))
                    return
            except (Psycopg2OpError, OperationalError):
                # 예외가 발생하면, 만약 마지막 시도인 경우 실패 메시지를 출력합니다.
                if i == 9:
                    self.stdout.write(self.style.ERROR(f"PostgreSQL Connection Failed after {i+1} attempts"))
                # 연결 실패 메시지와 함께 재시도 대기 메시지를 출력합니다.
                self.stdout.write(self.style.WARNING("PostgreSQL Connection Failed! Retrying in 1 second..."))
                # 1초 대기 후 다음 시도로 넘어갑니다.
                time.sleep(1)
