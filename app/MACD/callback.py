import json

from klines.kline import Klines
from klines.schema.kline import KlineSchema

from conf.redis_conf import server_redis
from conf.settings import settings


def macd_callback(klines: Klines, kline: KlineSchema):
    current_value = klines.current_MACD()
    predict = klines.predict_MACD()
    rev = klines.predict_MACD_reversal()

    # if rev:
    #     print(
    #         f"Разворот через {rev['step']} свечей ({rev['direction']})\n"
    #         f"Цена ≈ {rev['predicted_close']}, MACD={rev['macd']}, Signal={rev['signal']}"
    #     )

    data = {
        "kline_ms": kline.ts,
        "symbol": kline.symbol,
        "type": "MACD",
        "ex": settings.EXCHANGE,
        "data": {
            'current_value': current_value.model_dump_json(),
            'predict': [i.model_dump_json() for i in predict],
            'rev': rev
        }

    }
    massage = json.dumps(data).encode('utf-8')
    server_redis.publish(channel=f'signals:MACD:{settings.SYMBOL}', message=massage)
