import contextvars

from main import cache, models

request_var = contextvars.ContextVar("request", default=None)


def current_user():
    request = request_var.get()
    return getattr(request, "user_uid", None)


# 异步用户认证
async def async_auth(request):
    headers = request.headers
    auth_value = headers.get("Authorization")
    if not auth_value:
        return None
    parts = auth_value.split(" ")
    if parts[0].lower() != "bearer":
        return None
    token = " ".join(parts[1:])
    if not token:
        return None
    user_uid = await cache.User.get_by_token(token)
    if not user_uid:
        user = await models.User.objects.filter(uid=user_uid,
                                                token=token).afirst()
        if not user:
            return None
        cache.User.set_token(token, user.uid)
        user_uid = user.uid
    setattr(request, "token", token)
    setattr(request, "user_uid", user_uid)
    request_var.set(request)
    return token


# 异步用户认证（登录或未登录均可）
async def async_auth_optional(request):
    setattr(request, "token", "")
    setattr(request, "user_uid", "")
    headers = request.headers
    auth_value = headers.get("Authorization")
    if not auth_value:
        return "hh"
    parts = auth_value.split(" ")
    if parts[0].lower() != "bearer":
        return "hh"
    token = " ".join(parts[1:])
    if not token:
        return "hh"
    user_uid = await cache.User.get_by_token(token)
    if not user_uid:
        user = await models.User.objects.filter(token=token).afirst()
        if not user:
            return "hh"
        cache.User.set_token(token, user.uid)
        user_uid = user.uid
    setattr(request, "token", token)
    setattr(request, "user_uid", user_uid)
    request_var.set(request)
    return token
