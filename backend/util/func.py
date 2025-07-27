from argon2 import PasswordHasher

ph = PasswordHasher()


def encode_password(password: str) -> str:
    """
    패스워드 암호화

    Args:
        password (str): 평문 패스워드

    Returns:
        str: 암호화된 패스워드
    """
    return ph.hash(password)


def verify_password(password: str, encoded_password: str) -> bool:
    """
    패스워드 검증

    Args:
        password (str): 평문 패스워드
        encoded_password (str): 암호화된 패스워드

    Returns:
        bool: 패스워드 일치 여부(일치 시 True, 불일치 시 False)
    """
    try:
        ph.verify(encoded_password, password)
        return True
    except Exception as e:
        return False
