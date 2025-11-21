# /home/www/PROJECTS/TRAIDING/BACKEND/SIGNALS/app/RSI/stoch_rsi.py

from app.RSI.storage import STOCH_RSI_VALUES, STOCH_RSI_PREDICT
from app.RSI.utils import split_range


def get_signal(markers, interval: int, stoch) -> str | None:
    if not markers.actives.get(interval, False):
        return None

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
    if not markers.actives.get(kline.interval, False):
        STOCH_RSI_PREDICT[kline.interval] = None
        return

    index = markers.intervals.index(kline.interval)
    k_value = stoch.value[0]

    if k_value < 40:
        side = "buy"
        target_percent = markers.buy.predict[index]
    elif k_value > 60:
        side = "sell"
        target_percent = markers.sell.predict[index]
    else:
        STOCH_RSI_PREDICT[kline.interval] = None
        return

    prediction = klines.predict_stoch_rsi(
        side=side,
        target_range=target_percent,
        max_iter=max_iter,
    )

    # Проверка: предсказание должно оставаться в пределах target_percent от текущей цены
    if prediction:
        current_price = float(klines.history[-1].data[0].close)
        max_delta = current_price * target_percent / 100
        if abs(prediction.rate - current_price) > max_delta:
            prediction = None

    STOCH_RSI_PREDICT[kline.interval] = prediction

