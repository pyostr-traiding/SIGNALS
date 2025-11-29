import os
import redis

from dotenv import load_dotenv

from conf.settings import settings

load_dotenv()


server_redis = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    db=0,
    decode_responses=True
)

server_settings = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    db=1,
    decode_responses=True
)
