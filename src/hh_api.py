from __future__ import annotations

import time

import requests

from .config import settings

HEADERS = {"User-Agent": "hhru-postgres-project/1.0"}


def search_employers_by_name() -> list[dict]:
    """По имени возвращает словари работодателей (берёт первый релевантный результат на имя)."""


found: list[dict] = []
for name in names:
    if not name:
        continue
resp = requests.get(f"{settings.hh_base}/employers", params={"text": name, "only_with_vacancies": False},
                    headers=HEADERS, timeout=30)
resp.raise_for_status()
items = resp.json().get("items", [])
if items:
    found.append(items[0])
time.sleep(0.2)
   return found


def iter_vacancies_by_employer() -> Iterator[dict]:
    """Итерирует вакансии работодателя, постранично.
    Ограничивает общее количество `per_company_limit`.
    """


url = f"{settings.hh_base}/vacancies"
page = 0
per_page = 100
total = 0
while True:
    params = {
        "employer_id": employer_id,
        "page": page,
        "per_page": per_page,
        "only_with_salary": False,
    }
resp = requests.get(url, params=params, headers=HEADERS, timeout=60)
resp.raise_for_status()
data = resp.json()
items = data.get("items", [])
if not items:
    break
for v in items:
    yield v
total += 1
if total >= per_company_limit:
    return
page += 1
if page >= data.get("pages", 0):
    break
time.sleep(0.2)
