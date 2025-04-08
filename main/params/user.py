from ninja import Schema, Field


class CreateUserParam(Schema):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class LoginParam(Schema):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class ChangePasswordParam(Schema):
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., description="新密码")
