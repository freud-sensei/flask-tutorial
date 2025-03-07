# ORM 적용을 위한 데이터베이스 설정

import os

BASE_DIR = os.path.dirname(__file__)

# 데이터베이스 접속 주소
# DB 파일은 홈 디렉터리 바로 밑에 pybo.db 파일로 저장
SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "pybo.db")}'

# SQLAlchemy의 이벤트를 처리하는 옵션
SQLALCHEMY_TRACK_MODIFICATIONS = False

# CSRF 토큰: 취약점 공격을 방지
# 실제론 이런 문자열 쓰면 안 됨.
SECRET_KEY = "dev"