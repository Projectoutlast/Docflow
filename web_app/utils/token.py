from itsdangerous import URLSafeTimedSerializer

from config import Config


def generate_token(email: str) -> str:
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    return serializer.dumps(email, salt=Config.SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=3600) -> str | bool:
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    try:
        email = serializer.loads(token, salt=Config.SECURITY_PASSWORD_SALT, max_age=expiration)
        return email
    except Exception:
        return False
