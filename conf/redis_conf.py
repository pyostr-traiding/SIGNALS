import os
import redis

from dotenv import load_dotenv


load_dotenv()


server_redis = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT')),
    password=os.getenv('REDIS_PASSWORD'),
    db=0,
    decode_responses=True
)
