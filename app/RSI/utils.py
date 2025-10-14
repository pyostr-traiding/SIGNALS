def split_range(range_str: str) -> tuple[int, int]:
    """Разбивает строку диапазона '30-70' на кортеж (30, 70)."""
    return tuple(map(int, range_str.split('-')))