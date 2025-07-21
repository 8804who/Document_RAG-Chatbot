from pydantic import BaseModel, EmailStr


class User(BaseModel):
    user_id: str
    name: str
    email: EmailStr
