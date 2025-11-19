from typing import List

from pydantic import BaseModel


class ValuesSchema(BaseModel):
    """
    Схема значений
    """
    values: list
    predict: List[float]


class RSIMarkersSchema(BaseModel):
    """
    Схема настройки RSI метрик
    """
    buy: ValuesSchema
    sell: ValuesSchema
    intervals: List[int]
    is_active: bool
    actives: dict

