import json
import os

import redis

from dotenv import load_dotenv

from klines.kline import Klines
from klines.schema.kline import KlineSchema, CandleSchema

from conf.settings import settings

from app.callback import kline_callback

load_dotenv()

server_redis = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT')),
    password=os.getenv('REDIS_PASSWORD'),
    db=0,
    decode_responses=True
)

klines_1 = Klines(
    symbol=settings.SYMBOL,
    interval=1,
    exchange=settings.EXCHANGE,
    redis_candles=server_redis
)

klines_5 = Klines(
    symbol=settings.SYMBOL,
    interval=5,
    exchange=settings.EXCHANGE,
    redis_candles=server_redis
)

klines_15 = Klines(
    symbol=settings.SYMBOL,
    interval=15,
    exchange=settings.EXCHANGE,
    redis_candles=server_redis
)

klines_30 = Klines(
    symbol=settings.SYMBOL,
    interval=30,
    exchange=settings.EXCHANGE,
    redis_candles=server_redis
)

klines_60 = Klines(
    symbol=settings.SYMBOL,
    interval=60,
    exchange=settings.EXCHANGE,
    redis_candles=server_redis
)

klines_120 = Klines(
    symbol=settings.SYMBOL,
    interval=120,
    exchange=settings.EXCHANGE,
    redis_candles=server_redis
)


if __name__ == "__main__":

    pubsub = server_redis.pubsub()
    pubsub.subscribe(f'kline:{settings.SYMBOL}')
    while True:
        msg = pubsub.get_message()
        if msg and not isinstance(msg["data"], int):
            data = json.loads(msg['data'])['data']
            kline = KlineSchema(
                topic='1',
                symbol=data['symbol'],
                interval=data['interval'],
                data=[CandleSchema(
                    dt=data['data']['dt'],
                    start=data['data']['ts'],
                    interval=data['interval'],
                    open=data['data']['o'],
                    close=data['data']['c'],
                    high=data['data']['h'],
                    low=data['data']['l'],
                    volume=data['data']['v'],
                    turnover=data['data']['t'],
                )]
            )
            if kline.data[0].interval == 1:
                kline_callback(klines=klines_1, kline=kline)

            if kline.data[0].interval == 5:
                kline_callback(klines=klines_5, kline=kline)

            if kline.data[0].interval == 15:
                kline_callback(klines=klines_15, kline=kline)

            if kline.data[0].interval == 30:
                kline_callback(klines=klines_30, kline=kline)

            if kline.data[0].interval == 60:
                kline_callback(klines=klines_60, kline=kline)

            if kline.data[0].interval == 120:
                kline_callback(klines=klines_120, kline=kline)