from ninja import Router
from ninja.constants import NOT_SET
from django.db import IntegrityError
from django.contrib.auth.hashers import (
    make_password,
    check_password,
)

from main import (
    cache,
    models,
    params,
    results,
)
from main.response import (
    OkResponse,
    FailedResponse,
)
from main.auth import async_auth

user_router = Router(tags=["用户"])


@user_router.post("/signup",
                  auth=NOT_SET,
                  response=OkResponse[results.UserResult] | FailedResponse,
                  summary="| 注册")
async def CreateUserHandler(request, param: params.CreateUserParam):
    # 检查用户名是否已存在
    existing_user = await models.User.objects.filter(username=param.username
                                                     ).afirst()
    if existing_user:
        return FailedResponse(message="用户名已存在，请选择其他用户名")

    try:
        hashed_password = make_password(param.password)
        user = await models.User.objects.acreate(username=param.username,
                                                 password=hashed_password)
        return OkResponse(
            results.UserResult(uid=user.uid, username=user.username))
    except IntegrityError:
        return FailedResponse(message="用户名已存在，请选择其他用户名")


@user_router.post("/login",
                  auth=NOT_SET,
                  response=OkResponse[results.LoginResult],
                  summary="| 登录")
async def LoginHandler(request, param: params.LoginParam):
    user = await models.User.objects.filter(username=param.username).afirst()
    if not user or not check_password(param.password, user.password):
        return FailedResponse(message="用户名或密码错误")
    token = await cache.User.set_token(user.uid)
    return OkResponse(
        results.LoginResult(uid=user.uid, username=user.username, token=token))


@user_router.get("/logout",
                 auth=async_auth,
                 response=OkResponse,
                 summary="| 登出")
async def LogoutHandler(request):
    await cache.User.delete_token(request.token)
    return OkResponse()


@user_router.post("/change_password",
                  auth=async_auth,
                  response=OkResponse,
                  summary="| 修改密码")
async def ChangePasswordHandler(request, param: params.ChangePasswordParam):
    user = await models.User.objects.filter(uid=request.user_uid).afirst()
    if not user:
        return FailedResponse(message="用户名或密码错误")
    if not check_password(param.old_password, user.password):
        return FailedResponse(message="用户名或密码错误")
    user.password = make_password(param.new_password)
    await user.asave(update_fields=["password"])
    return OkResponse()
