from ninja import Schema, Field


class UserResult(Schema):
    uid: str = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")


class LoginResult(Schema):
    uid: str = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    token: str = Field(..., description="token")
