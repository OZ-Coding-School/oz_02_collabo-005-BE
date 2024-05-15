import re
from django.core.exceptions import ValidationError

def validate_password(value):
    password_regex = re.compile(r'^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*?_]).{8,16}$')
    if not password_regex.match(value):
        raise ValidationError("비밀번호는 영문, 숫자, 특수문자를 포함하여 8~16자여야 합니다.")
    if ' ' in value:
        raise ValidationError("패스워드는 공백을 포함할 수 없습니다.")
    return value

def validate_phone_number(value):
    phone_regex = re.compile(r'^010\d{8}$')
    if not phone_regex.match(value):
        raise ValidationError("유효하지 않은 휴대폰 번호 형식입니다.")
    return value

def validate_birthday(value):
    birthday_regex = re.compile(r'^\d{4}\d{2}\d{2}$')
    if not birthday_regex.match(value):
        raise ValidationError("유효하지 않은 생년월일 형식입니다.")
    return value