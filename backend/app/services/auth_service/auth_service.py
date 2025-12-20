from abc import ABC, abstractmethod

class AuthService(ABC):
    def __init__(self):
        pass


    @abstractmethod
    async def verify_token(self, token: str) -> bool:
        pass


    @abstractmethod
    async def verify_id_token(self, id_token: str) -> dict:
        pass


    @abstractmethod
    async def save_token(self, name: str, email: str, refresh_token: str) -> None:
        pass


    @abstractmethod
    async def get_token(self, email: str) -> str:
        pass
