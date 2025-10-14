from app.RSI.storage import RSI_VALUES, RSI_PREDICT, STOCH_RSI_PREDICT, STOCH_RSI_VALUES

from app.RSI.rsi import get_signal as get_rsi_signal
from app.RSI.stoch_rsi import get_signal as get_stoch_signal


# Проверка сигналов на вход по текущим значениям (RSI или Stoch RSI)
def check_entry(
        storage: dict,
        signal_fn,
        name: str,
        markers
):
    if not all(storage.values()):  # Не все значения получены — выходим
        return
    # Считаем сигналы для всех интервалов
    signals = [signal_fn(markers, interval, value)
               for interval, value in storage.items()
               if value]
    # Если сигналы одинаковы и есть для всех интервалов — выводим сигнал
    if len(signals) == len(storage) and len(set(signals)) == 1:
        print(f"{name} ENTRY:", signals[0])

# Проверка предсказанных сигналов
def check_predict(
        predict_storage,
        value_storage,
        signal_fn,
        name: str,
        markers,
):
    if not all(predict_storage.values()):  # Не все предсказания есть
        return
    signals = []
    for interval, _ in predict_storage.items():
        value = value_storage.get(interval)
        if not value:  # Отсутствует текущее значение для интервала
            return
        signal = signal_fn(markers, interval, value)
        if signal:
            signals.append(signal)
    # Если все сигналы есть и одинаковы — выводим предсказанный сигнал
    if len(signals) == len(predict_storage) and len(set(signals)) == 1:
        print(f"{name} PREDICT:", signals[0])

# Проверка всех сигналов: RSI и Stoch RSI (текущие и предсказанные)
def check_all(rsi_markers, stoch_rsi_markers):
    check_entry(RSI_VALUES, get_rsi_signal, "RSI", markers=rsi_markers)
    check_predict(RSI_PREDICT, RSI_VALUES, get_rsi_signal, "RSI", markers=rsi_markers)
    check_entry(STOCH_RSI_VALUES, get_stoch_signal, "STOCH", markers=stoch_rsi_markers)
    check_predict(STOCH_RSI_PREDICT, STOCH_RSI_VALUES, get_stoch_signal, "STOCH",markers=stoch_rsi_markers)
