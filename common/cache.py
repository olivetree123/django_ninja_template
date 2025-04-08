from typing import Any, Optional

from django.conf import settings
from redis.asyncio import Redis


class BaseCache:
    """缓存基类"""
    PREFIX = ""  # 缓存前缀
    EXPIRE = 24 * 60 * 60  # 过期时间(秒)

    @classmethod
    def get_redis(cls) -> Redis:
        """获取redis连接"""
        if not hasattr(cls, '_redis'):
            cls._redis = Redis(host=settings.REDIS_HOST,
                               port=settings.REDIS_PORT,
                               db=0,
                               decode_responses=True)
        return cls._redis

    @classmethod
    def get_key(cls, key: str) -> str:
        """获取完整的缓存key"""
        return f"{cls.PREFIX}:{key}" if cls.PREFIX else key

    @classmethod
    async def get(cls, key: str) -> Any:
        """获取缓存"""
        redis = cls.get_redis()
        return await redis.get(cls.get_key(key))

    @classmethod
    async def set(cls,
                  key: str,
                  value: Any,
                  expire: Optional[int] = None) -> None:
        """设置缓存"""
        redis = cls.get_redis()
        await redis.set(cls.get_key(key),
                        value,
                        ex=expire if expire is not None else cls.EXPIRE)

    @classmethod
    async def delete(cls, key: str) -> None:
        """删除缓存"""
        redis = cls.get_redis()
        await redis.delete(cls.get_key(key))

    @classmethod
    async def exists(cls, key: str) -> bool:
        """判断缓存是否存在"""
        redis = cls.get_redis()
        return await redis.exists(cls.get_key(key))

    @classmethod
    async def expire(cls, key: str, seconds: int) -> None:
        """设置过期时间"""
        redis = cls.get_redis()
        await redis.expire(cls.get_key(key), seconds)

    @classmethod
    async def ttl(cls, key: str) -> int:
        """获取剩余过期时间"""
        redis = cls.get_redis()
        return await redis.ttl(cls.get_key(key))

    @classmethod
    async def incr(cls, key: str, amount: int = 1) -> int:
        """递增"""
        redis = cls.get_redis()
        return await redis.incr(cls.get_key(key), amount)

    @classmethod
    async def decr(cls, key: str, amount: int = 1) -> int:
        """递减"""
        redis = cls.get_redis()
        return await redis.decr(cls.get_key(key), amount)

    @classmethod
    async def hget(cls, name: str, key: str) -> Any:
        """获取hash值"""
        redis = cls.get_redis()
        return await redis.hget(cls.get_key(name), key)

    @classmethod
    async def hset(cls, name: str, key: str, value: Any) -> None:
        """设置hash值"""
        redis = cls.get_redis()
        await redis.hset(cls.get_key(name), key, value)

    @classmethod
    async def hdel(cls, name: str, *keys: str) -> None:
        """删除hash值"""
        redis = cls.get_redis()
        await redis.hdel(cls.get_key(name), *keys)

    @classmethod
    async def hgetall(cls, name: str) -> dict:
        """获取所有hash值"""
        redis = cls.get_redis()
        return await redis.hgetall(cls.get_key(name))

    @classmethod
    async def sadd(cls, name: str, *values: Any) -> None:
        """添加set成员"""
        redis = cls.get_redis()
        await redis.sadd(cls.get_key(name), *values)

    @classmethod
    async def srem(cls, name: str, *values: Any) -> None:
        """删除set成员"""
        redis = cls.get_redis()
        await redis.srem(cls.get_key(name), *values)

    @classmethod
    async def smembers(cls, name: str) -> set:
        """获取所有set成员"""
        redis = cls.get_redis()
        return await redis.smembers(cls.get_key(name))

    @classmethod
    async def sismember(cls, name: str, value: Any) -> bool:
        """判断是否是set成员"""
        redis = cls.get_redis()
        return await redis.sismember(cls.get_key(name), value)

    @classmethod
    async def zadd(cls, name: str, mapping: dict) -> None:
        """添加有序集合成员"""
        redis = cls.get_redis()
        await redis.zadd(cls.get_key(name), mapping)

    @classmethod
    async def zrem(cls, name: str, *values: Any) -> None:
        """删除有序集合成员"""
        redis = cls.get_redis()
        await redis.zrem(cls.get_key(name), *values)

    @classmethod
    async def zrange(cls,
                     name: str,
                     start: int,
                     end: int,
                     desc: bool = False) -> list:
        """获取有序集合范围内的成员"""
        redis = cls.get_redis()
        return await redis.zrange(cls.get_key(name), start, end, desc=desc)

    @classmethod
    async def zrangebyscore(cls, name: str, min_score: float,
                            max_score: float) -> list:
        """获取有序集合分数范围内的成员"""
        redis = cls.get_redis()
        return await redis.zrangebyscore(cls.get_key(name), min_score,
                                         max_score)
