from __future__ import annotations
from typing import Optional

SUPPORTED_CURRENCY = {"RUR"}

def calc_salary_avg(salary: dict | None) -> tuple[Optional[str], Optional[float], Optional[float], Optional[float]]:
    """
    Возвращает (currency, from, to, avg).
    Если валюта не SUPPORTED_CURRENCY — возвращает None-значения.
    HH salary: {from: int|None, to: int|None, currency: str|None}
    """
    if not salary:
        return None, None, None, None

    currency = salary.get("currency")
    if currency not in SUPPORTED_CURRENCY:
        return currency, None, None, None

    f = salary.get("from")
    t = salary.get("to")

    if f is None and t is None:
        return currency, None, None, None

    if f is None:
        avg = float(t)
    elif t is None:
        avg = float(f)
    else:
        avg = (float(f) + float(t)) / 2.0

    return currency, float(f) if f is not None else None, float(t) if t is not None else None, avg
