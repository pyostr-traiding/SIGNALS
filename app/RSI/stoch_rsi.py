# /home/www/PROJECTS/TRAIDING/BACKEND/SIGNALS/app/RSI/stoch_rsi.py

from app.RSI.storage import STOCH_RSI_VALUES, STOCH_RSI_PREDICT
from app.RSI.utils import split_range


def get_signal(markers, interval: int, stoch) -> str | None:
    """
    Получает торговый сигнал на основе значения Stochastic RSI (%K)
    """
    index = markers.intervals.index(interval)
    k_value = stoch.value[0]

    low, high = split_range(markers.buy.values[index])
    if low <= k_value <= high:
        STOCH_RSI_VALUES[interval] = stoch
        return "buy"

    low, high = split_range(markers.sell.values[index])
    if low <= k_value <= high:
        STOCH_RSI_VALUES[interval] = stoch
        return "sell"

    STOCH_RSI_VALUES[interval] = None
    return None


def update_prediction(klines, kline, stoch, markers, max_iter: int = 40) -> None:
    """
    Предсказывает цену, при которой %K из Stochastic RSI попадёт в заданный диапазон.
    Использует markers.predict[index] как target для бинарного поиска.
    """
    index = markers.intervals.index(kline.interval)
    k_value = stoch.value[0]

    if k_value < 40:
        side = "buy"
        target = markers.buy.predict[index]
    elif k_value > 60:
        side = "sell"
        target = markers.sell.predict[index]
    else:
        STOCH_RSI_PREDICT[kline.interval] = None
        return

    prediction = klines.predict_stoch_rsi(
        side=side,
        target_range=target,
        max_iter=max_iter,
    )
    STOCH_RSI_PREDICT[kline.interval] = prediction or None
