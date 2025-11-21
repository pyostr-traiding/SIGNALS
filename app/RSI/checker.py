# /home/www/PROJECTS/TRAIDING/BACKEND/SIGNALS/app/RSI/checker.py

from app.RSI.storage import (
    RSI_VALUES,
    RSI_PREDICT,
    STOCH_RSI_PREDICT,
    STOCH_RSI_VALUES,
)

from app.RSI.rsi import get_signal as get_rsi_signal
from app.RSI.stoch_rsi import get_signal as get_stoch_signal


def check_entry(storage: dict, signal_fn, name: str, markers) -> None:
    """
    Проверка сигналов по текущим значениям (RSI или Stoch RSI)
    """
    if not storage:
        return

    if not all(storage.values()):
        return

    signals = [
        signal_fn(markers, interval, value)
        for interval, value in storage.items()
        if value
    ]

    if len(signals) == len(storage) and len(set(signals)) == 1 and signals[0]:
        print(f"{name} ENTRY:", signals[0])


def check_predict(
    predict_storage: dict,
    value_storage: dict,
    signal_fn,
    name: str,
    markers,
) -> None:
    """
    Проверка предсказанных сигналов
    """
    if not predict_storage:
        return

    if not all(predict_storage.values()):
        return

    signals = []
    for interval, _ in predict_storage.items():
        value = value_storage.get(interval)
        if not value:
            return
        signal = signal_fn(markers, interval, value)
        if signal:
            signals.append(signal)

    if len(signals) == len(predict_storage) and len(set(signals)) == 1:
        print(f"{name} PREDICT:", signals[0])


def check_all(rsi_markers, stoch_rsi_markers) -> None:
    """
    Проверка RSI и Stoch RSI (текущие и предсказанные)
    """
    check_entry(RSI_VALUES, get_rsi_signal, "RSI", markers=rsi_markers)
    check_predict(RSI_PREDICT, RSI_VALUES, get_rsi_signal, "RSI", markers=rsi_markers)

    check_entry(STOCH_RSI_VALUES, get_stoch_signal, "STOCH", markers=stoch_rsi_markers)
    check_predict(
        STOCH_RSI_PREDICT,
        STOCH_RSI_VALUES,
        get_stoch_signal,
        "STOCH",
        markers=stoch_rsi_markers,
    )
