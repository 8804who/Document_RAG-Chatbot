class AuthService:
    def __init__(self):
        pass


    async def verify_token(self, token: str) -> bool:
        pass


    async def verify_id_token(self, id_token: str) -> bool:
        pass


    async def save_token(self, name: str, email: str, refresh_token: str) -> bool:
        pass


    async def get_token(self, email: str) -> str:
        pass
