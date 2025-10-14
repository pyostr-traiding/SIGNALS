from app.signals.storage import RSI_VALUES, RSI_PREDICT, STOCH_RSI_VALUES, STOCH_RSI_PREDICT

# Обновление интервалов, которые должны быть активны в хранилищах сигналов и предсказаний
def update_enabled_intervals(enabled_intervals: list[int]):
    for storage in (RSI_VALUES, RSI_PREDICT, STOCH_RSI_VALUES, STOCH_RSI_PREDICT):
        # Удаляем неактуальные интервалы
        for key in list(storage.keys()):
            if key not in enabled_intervals:
                storage.pop(key, None)
        # Добавляем недостающие интервалы со значением по умолчанию
        for interval in enabled_intervals:
            storage.setdefault(interval, None)
