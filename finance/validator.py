import re
from django.core.exceptions import ValidationError

def validate_password(password):
    if len(password) < 6 or len(password) > 12:
        raise ValidationError('비밀번호는 6자 이상 12자 이하여야 합니다.')
    if not re.search(r'[A-Z]', password):
        raise ValidationError('비밀번호에 하나 이상의 대문자가 포함되어야 합니다.')
    if not re.search(r'[a-z]', password):
        raise ValidationError('비밀번호에 하나 이상의 소문자가 포함되어야 합니다.')