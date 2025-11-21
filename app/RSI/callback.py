# /home/www/PROJECTS/TRAIDING/BACKEND/SIGNALS/app/RSI/callback.py

import json
from datetime import datetime

from cachetools import TTLCache, cached
from klines.schema.kline import KlineSchema

from app.RSI.checker import check_all
from app.RSI.schema import RSIMarkersSchema
from app.RSI.storage import (
    RSI_VALUES,
    RSI_PREDICT,
    STOCH_RSI_VALUES,
    STOCH_RSI_PREDICT,
)
from conf.redis_conf import server_redis, server_settings
from conf.settings import settings
from app.RSI.rsi import get_signal as rsi_signal, update_prediction as rsi_predict
from app.RSI.stoch_rsi import get_signal as stoch_signal, update_prediction as stoch_predict

rsi_cache = TTLCache(maxsize=100, ttl=5)
stoch_rsi_cache = TTLCache(maxsize=100, ttl=5)


@cached(cache=rsi_cache)
def get_and_load_RSI_markers() -> RSIMarkersSchema:
    data = server_settings.get("settings:indicator:RSI")
    data = json.loads(data)
    data["actives"] = {i: True for i in data["intervals"]}
    markers = RSIMarkersSchema(**data)

    for key, value in markers.actives.items():
        ikey = int(key)
        if value:
            RSI_VALUES.setdefault(ikey, None)
            RSI_PREDICT.setdefault(ikey, None)
        else:
            RSI_VALUES.pop(ikey, None)
            RSI_PREDICT.pop(ikey, None)
    return markers


@cached(cache=stoch_rsi_cache)
def get_and_load_Stoch_RSI_markers() -> RSIMarkersSchema:
    data = server_settings.get("settings:indicator:STOCH_RSI")
    data = json.loads(data)
    data["actives"] = {i: True for i in data["intervals"]}
    markers = RSIMarkersSchema(**data)

    for key, value in markers.actives.items():
        ikey = int(key)
        if value:
            STOCH_RSI_VALUES.setdefault(ikey, None)
            STOCH_RSI_PREDICT.setdefault(ikey, None)
        else:
            STOCH_RSI_VALUES.pop(ikey, None)
            STOCH_RSI_PREDICT.pop(ikey, None)
    return markers


def rsi_callback(klines, kline: KlineSchema) -> None:
    rsi_markers = get_and_load_RSI_markers()
    stoch_rsi_markers = get_and_load_Stoch_RSI_markers()

    # INFO по маркерам
    info_payload = {
        "kline_ms": kline.ts,
        "symbol": kline.symbol,
        "type": "INFO",
        "ex": settings.EXCHANGE,
        "RSI": rsi_markers.model_dump(),
        "StochRSI": stoch_rsi_markers.model_dump(),
    }
    message = json.dumps(info_payload).encode("utf-8")
    server_redis.publish(
        channel=f"signals:{settings.SYMBOL}:INFO",
        message=message,
    )

    # Проверки активности
    if not rsi_markers:
        if settings.PRINT_DEBUG:
            print(f"[{datetime.now()}] Маркеры RSI не получены\n{rsi_markers}")
        return
    if not rsi_markers.is_active:
        if settings.PRINT_DEBUG:
            print(f"[{datetime.now()}] Маркеры RSI отключены\n{rsi_markers}")
        return

    if not stoch_rsi_markers:
        if settings.PRINT_DEBUG:
            print(f"[{datetime.now()}] Маркеры Stoch RSI не получены\n{stoch_rsi_markers}")
        return
    if not stoch_rsi_markers.is_active:
        if settings.PRINT_DEBUG:
            print(f"[{datetime.now()}] Маркеры Stoch RSI отключены\n{stoch_rsi_markers}")
        return

    if kline.interval not in STOCH_RSI_PREDICT:
        if settings.PRINT_DEBUG:
            print(f"[{datetime.now()}] Интервал [{kline.interval}] отключен. Игнор.\n")
        return

    # --- Текущие значения ---
    rsi = klines.current_RSI()
    rsi_signal(rsi_markers, klines.interval, rsi)
    rsi_predict(klines, kline, rsi, rsi_markers)

    stoch = klines.current_stoch_RSI()
    stoch_signal(stoch_rsi_markers, klines.interval, stoch)
    stoch_predict(klines, kline, stoch, stoch_rsi_markers)

    # --- Проверка согласованности сигналов по всем интервалам ---
    check_all(
        rsi_markers=rsi_markers,
        stoch_rsi_markers=stoch_rsi_markers,
    )

    # print("------------------")
    print("RSI:", RSI_VALUES)
    print("RSI_PREDICT:", RSI_PREDICT)
    print("STOCH:", STOCH_RSI_VALUES)
    print("STOCH_PREDICT:", STOCH_RSI_PREDICT)

    # --- Отправка предсказаний RSI ---
    rsi_predict_values = [
        {
            "kline_ms": value.kline_ms,
            "interval": value.interval,
            "value": value.rsi,
            "side": value.side,
            "percent": value.percent,
            "target_rate": value.rate,
        }
        for _, value in RSI_PREDICT.items()
        if value
    ]

    rsi_payload = {
        "kline_ms": kline.ts,
        "symbol": kline.symbol,
        "type": "PREDICT.RSI",
        "ex": settings.EXCHANGE,
        "values": rsi_predict_values,
    }
    message = json.dumps(rsi_payload).encode("utf-8")
    server_redis.publish(
        channel=f"signals:{settings.SYMBOL}",
        message=message,
    )

    # --- Отправка предсказаний STOCH_RSI ---
    stoch_predict_values = [
        {
            "kline_ms": value.kline_ms,
            "interval": value.interval,
            "value_k": value.k,
            "value_d": value.d,
            "side": value.side,
            "percent": value.percent,
            "target_rate": value.rate,
        }
        for _, value in STOCH_RSI_PREDICT.items()
        if value
    ]

    stoch_payload = {
        "kline_ms": kline.ts,
        "symbol": kline.symbol,
        "type": "PREDICT.STOCH_RSI",
        "ex": settings.EXCHANGE,
        "values": stoch_predict_values,
    }
    message = json.dumps(stoch_payload).encode("utf-8")
    server_redis.publish(
        channel=f"signals:{settings.SYMBOL}",
        message=message,
    )
