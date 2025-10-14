from app.RSI.storage import STOCH_RSI_VALUES, STOCH_RSI_PREDICT
from app.RSI.utils import split_range


# Получает торговый сигнал на основе значения Stochastic RSI (%K)
def get_signal(markers, interval: int, stoch) -> str | None:
    index = markers.intervals.index(interval)
    k_value = stoch.value[0]  # Берём значение %K

    # Проверка на диапазон покупки
    low, high = split_range(markers.buy.values[index])
    if low <= k_value <= high:
        STOCH_RSI_VALUES[interval] = stoch
        return 'buy'

    # Проверка на диапазон продажи
    low, high = split_range(markers.sell.values[index])
    if low <= k_value <= high:
        STOCH_RSI_VALUES[interval] = stoch
        return 'sell'

    # Если нет сигнала — очищаем значение
    STOCH_RSI_VALUES[interval] = None
    return None

# Предсказывает цену, при которой Stochastic RSI попадёт в заданный диапазон
def update_prediction(klines, kline, stoch, markers):
    index = markers.intervals.index(kline.interval)
    k_value = stoch.value[0]  # Используем %K

    # Определяем направление предсказания
    if k_value < 40:
        side, target = 'buy', markers.buy.values[index]
    elif k_value > 60:
        side, target = 'sell', markers.sell.values[index]
    else:
        STOCH_RSI_PREDICT[kline.interval] = None
        return

    # Получаем предсказание и сохраняем
    prediction = klines.predict_stoch_rsi(side=side, target_range=target)
    STOCH_RSI_PREDICT[kline.interval] = prediction or None
