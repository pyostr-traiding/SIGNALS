import json
from pprint import pprint

from klines.kline import Klines
from klines.schema.kline import KlineSchema

from conf.redis_conf import server_redis
from conf.settings import settings


def adx_callback(klines: Klines, kline: KlineSchema):
    current_value = klines.current_ADX()

    data = {
        "kline_ms": kline.ts,
        "symbol": kline.symbol,
        "type": "MACD",
        "ex": settings.EXCHANGE,
        "data": {
            'current_value': current_value.model_dump_json(),
        }
    }
    pprint(data)
    massage = json.dumps(data).encode('utf-8')
    server_redis.publish(channel=f'signals:ADX:{settings.SYMBOL}', message=massage)
