import json
from typing import Optional, List, Dict

from django.conf import settings

from common.cache import BaseCache
from main import results

get_user_token_key = lambda token: f"{settings.PROJECT.upper()}:USER_TOKEN:{token}"
get_user_detail_key = lambda user_uid: f"{settings.PROJECT.upper()}:USER:{user_uid}:DETAIL"


class User(BaseCache):
    """用户缓存"""

    @classmethod
    async def delete_token(cls, token: str) -> None:
        """删除用户token"""
        await cls.get_redis().delete(get_user_token_key(token))

    @classmethod
    async def set_token(cls, token: str, user_uid: str) -> None:
        """设置用户token"""
        await cls.get_redis().set(get_user_token_key(token), user_uid)

    @classmethod
    async def get_by_token(cls, token: str) -> Optional[str]:
        """获取用户信息"""
        return await cls.get_redis().get(get_user_token_key(token))

    @classmethod
    async def set_user(cls, user_uid: str, user: results.UserResult) -> None:
        """设置用户信息"""
        key = get_user_detail_key(user_uid)
        if not user:
            return
        await cls.get_redis().set(key, json.dumps(user.dict()), ex=cls.EXPIRE)

    @classmethod
    async def get_user(cls, user_uid: str) -> Optional[results.UserResult]:
        """获取用户信息"""
        key = get_user_detail_key(user_uid)
        data = await cls.get_redis().get(key)
        if not data:
            return None
        return results.UserResult(**json.loads(data))

    @classmethod
    async def del_user(cls, user_uid: str) -> None:
        """删除用户信息"""
        await cls.get_redis().delete(get_user_detail_key(user_uid))

    @classmethod
    async def get_user_multi(cls,
                             user_uid_list: List[str]) -> List[Optional[Dict]]:
        """批量获取用户信息"""
        pipe = cls.get_redis().pipeline()
        for user_uid in user_uid_list:
            pipe.hgetall(get_user_detail_key(user_uid))
        return await pipe.execute()
