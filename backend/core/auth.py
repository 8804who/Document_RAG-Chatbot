from crud import user as user_crud
from ..util import func
from fastapi import HTTPException


def login(username: str, password: str) -> bool:
    """
    유저 로그인 정보 검증

    Args:
        username (str): 사용자가 입력한 username
        password (str): 사용자가 입력한 패스워드

    Retunrs:
        bool: 유저 로그인 정보 일치 여부(일치 시 True, 불일치 시 False)
    """
    user_info = user_crud.get_user_info(username=username)

    encoded_password = func.encode_password(password)

    if username == user_info.username and func.verify_password(
        password, encoded_password
    ):
        return True
    else:
        raise HTTPException(status_code=401, detail="계정 정보가 일치하지 않습니다")
