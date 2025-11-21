# /home/www/PROJECTS/TRAIDING/BACKEND/SIGNALS/app/RSI/rsi.py

from app.RSI.storage import RSI_VALUES, RSI_PREDICT
from app.RSI.utils import split_range


def get_signal(markers, interval: int, rsi) -> str | None:
    """
    Определяет сигнал по текущему RSI и сохраняет его
    """
    if not markers.actives.get(interval, False):
        # Интервал отключен, игнорируем
        return None

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
    Использует markers.predict[index] как target для бинарного поиска.
    """
    if not markers.actives.get(kline.interval, False):
        RSI_PREDICT[kline.interval] = None
        return
    index = markers.intervals.index(kline.interval)

    value = rsi.value

    # Определяем сторону и target для бинарного поиска
    if value < 40:
        side = "buy"
        target = markers.buy.predict[index]  # float
    elif value > 60:
        side = "sell"
        target = markers.sell.predict[index]
    else:
        RSI_PREDICT[kline.interval] = None
        return

    prediction = klines.predict_rsi(
        side=side,
        rsi=value,
        target_range=target,  # float, без split
        max_iter=max_iter,
    )
    RSI_PREDICT[kline.interval] = prediction or None
