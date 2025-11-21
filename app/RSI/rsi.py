# /home/www/PROJECTS/TRAIDING/BACKEND/SIGNALS/app/RSI/rsi.py

from app.RSI.storage import RSI_VALUES, RSI_PREDICT
from app.RSI.utils import split_range


def get_signal(markers, interval: int, rsi) -> str | None:
    """
    Определяет сигнал по текущему RSI и сохраняет его
    """
    index = markers.intervals.index(interval)

    low, high = split_range(markers.buy.values[index])
    if low <= rsi.value <= high:
        RSI_VALUES[interval] = rsi
        return "buy"

    low, high = split_range(markers.sell.values[index])
    if low <= rsi.value <= high:
        RSI_VALUES[interval] = rsi
        return "sell"

    RSI_VALUES[interval] = None
    return None


def update_prediction(klines, kline, rsi, markers, max_iter: int = 40) -> None:
    """
    Предсказывает цену, при которой RSI попадёт в заданный диапазон.
    Внутри klines.predict_rsi используется бинарный поиск (без 2000 итераций).
    """
    index = markers.intervals.index(kline.interval)
    value = rsi.value

    if value < 40:
        side, target = "buy", markers.buy.values[index]
    elif value > 60:
        side, target = "sell", markers.sell.values[index]
    else:
        RSI_PREDICT[kline.interval] = None
        return

    prediction = klines.predict_rsi(
        side=side,
        rsi=value,
        target_range=target,
    )
    RSI_PREDICT[kline.interval] = prediction or None
