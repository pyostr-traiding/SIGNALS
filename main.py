import json

from dotenv import load_dotenv
from klines.kline import Klines
from klines.schema.kline import KlineSchema, CandleSchema

from app.MACD.callback import macd_callback
from conf.redis_conf import server_redis
from conf.settings import settings
from app.RSI.callback import rsi_callback

load_dotenv()

# Инициализация Klines для всех интервалов
intervals = [1, 5, 15, 30, 60, 120]
klines_map: dict[int, Klines] = {}

for interval in intervals:
    klines_map[interval] = Klines(
        symbol=settings.SYMBOL,
        interval=interval,
        exchange=settings.EXCHANGE,
        redis_candles=server_redis,
    )

def handle_message(message: dict):
    """Обрабатывает входящее сообщение Redis Pub/Sub."""
    if message["type"] != "message":
        return  # пропускаем служебные сообщения
    try:
        payload = json.loads(message["data"])
        data = payload["data"]
        kline = KlineSchema(
            ts=data["data"]["ts"],
            topic="1",
            symbol=data["symbol"],
            interval=data["interval"],
            data=[
                CandleSchema(
                    dt=data["data"]["dt"],
                    start=data["data"]["ts"],
                    interval=data["interval"],
                    open=data["data"]["o"],
                    close=data["data"]["c"],
                    high=data["data"]["h"],
                    low=data["data"]["l"],
                    volume=data["data"]["v"],
                    turnover=data["data"]["t"],
                )
            ],
        )

        interval = kline.data[0].interval
        klines_obj = klines_map.get(interval)
        if klines_obj:
            klines_obj.update(kline)
            rsi_callback(klines=klines_obj, kline=kline)
            macd_callback(klines=klines_obj, kline=kline)
    except Exception as e:
        print(f"[!] Ошибка обработки сообщения: {e}")


if __name__ == "__main__":
    print(f"Запуск RSI для {settings.SYMBOL}")
    pubsub = server_redis.pubsub()
    pubsub.subscribe(f"kline:{settings.SYMBOL}")

    try:
        # Главный блокирующий цикл — без нагрузки на CPU
        for message in pubsub.listen():
            handle_message(message)
    except KeyboardInterrupt:
        print("Остановка по Ctrl+C")
    except Exception as e:
        print(f"[!] Ошибка в основном цикле: {e}")
