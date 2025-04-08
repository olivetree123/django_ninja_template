import json
from typing import Optional, List, Dict

from django.conf import settings

from common.cache.base import Cache
from common import results

USER_TOKEN_KEY = lambda token: f"{settings.PROJECT.upper()}:USER_TOKEN:{token}"
USER_DETAIL_KEY = lambda user_uid: f"{settings.PROJECT.upper()}:USER:{user_uid}:DETAIL"


class User(Cache):
    """用户缓存"""

    @classmethod
    async def delete(cls, token: str) -> None:
        """删除用户token"""
        await cls.get_redis().delete(USER_TOKEN_KEY(token))

    @classmethod
    async def set_token(cls, token: str, user_uid: str) -> None:
        """设置用户token"""
        await cls.get_redis().set(USER_TOKEN_KEY(token), user_uid)

    @classmethod
    async def get_by_token(cls, token: str) -> Optional[str]:
        """获取用户信息"""
        return await cls.get_redis().get(USER_TOKEN_KEY(token))

    @classmethod
    async def set_user(cls, user_uid: str, user: results.UserResult) -> None:
        """设置用户信息"""
        key = USER_DETAIL_KEY(user_uid)
        if not user:
            return
        await cls.get_redis().set(key, json.dumps(user.dict()), ex=cls.EXPIRE)

    @classmethod
    async def get_user(cls, user_uid: str) -> Optional[results.UserResult]:
        """获取用户信息"""
        key = USER_DETAIL_KEY(user_uid)
        data = await cls.get_redis().get(key)
        if not data:
            return None
        return results.UserResult(**json.loads(data))

    @classmethod
    async def del_user(cls, user_uid: str) -> None:
        """删除用户信息"""
        await cls.get_redis().delete(USER_DETAIL_KEY(user_uid))

    @classmethod
    async def get_user_multi(cls,
                             user_uid_list: List[str]) -> List[Optional[Dict]]:
        """批量获取用户信息"""
        pipe = cls.get_redis().pipeline()
        for user_uid in user_uid_list:
            pipe.hgetall(USER_DETAIL_KEY(user_uid))
        return await pipe.execute()
