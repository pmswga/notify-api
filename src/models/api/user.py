from pydantic import BaseModel


class UserRegisterIn(BaseModel):
    username: str


class UserLogin(BaseModel):
    username: str


class UserRegisteredOut(BaseModel):
    user_id: int
    access: str
    refresh: str
