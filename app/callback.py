from klines.kline import Klines
from klines.schema.kline import KlineSchema


def kline_callback(klines: Klines, kline: KlineSchema):
    klines.update(kline)
    print(klines.length, len(klines.history), klines.last_kline)