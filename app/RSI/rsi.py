from app.RSI.storage import RSI_VALUES, RSI_PREDICT
from app.RSI.utils import split_range


# Определяет сигнал по текущему RSI и сохраняет его
def get_signal(markers, interval: int, rsi) -> str | None:
    index = markers.intervals.index(interval)

    # Проверка на диапазон покупки
    low, high = split_range(markers.buy.values[index])
    if low <= rsi.value <= high:
        RSI_VALUES[interval] = rsi
        return 'buy'

    # Проверка на диапазон продажи
    low, high = split_range(markers.sell.values[index])
    if low <= rsi.value <= high:
        RSI_VALUES[interval] = rsi
        return 'sell'

    # Если ни в один диапазон не попал — очищаем значение
    RSI_VALUES[interval] = None
    return None

# Предсказывает цену, при которой RSI попадёт в заданный диапазон
def update_prediction(klines, kline, rsi, markers):
    index = markers.intervals.index(kline.interval)
    value = rsi.value

    # Определяем направление и диапазон предсказания
    if value < 40:
        side, target = 'buy', markers.buy.values[index]
    elif value > 60:
        side, target = 'sell', markers.sell.values[index]
    else:
        RSI_PREDICT[kline.interval] = None
        return

    # Получаем предсказание и сохраняем
    prediction = klines.predict_rsi(side=side, target_range=target, rsi=value)
    RSI_PREDICT[kline.interval] = prediction or None
