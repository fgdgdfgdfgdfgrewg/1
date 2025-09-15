from __future__ import annotations
import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()

def _read_companies() -> tuple[str, ...]:
    raw = os.getenv("HH_COMPANIES", "").strip()
    if not raw:
        return tuple()
    return tuple(s.strip() for s in raw.split(","))

@dataclass(frozen=True)
class Settings:
    host: str = os.getenv("PG_HOST", "localhost")
    port: int = int(os.getenv("PG_PORT", "5432"))
    user: str = os.getenv("PG_USER", "postgres")
    password: str = os.getenv("PG_PASSWORD", "postgres")
    dbname: str = os.getenv("PG_DBNAME", "hh_project")

    hh_base: str = os.getenv("HH_API_BASE", "https://api.hh.ru")
    # ключ: неизменяемый тип + фабрика
    hh_companies: tuple[str, ...] = field(default_factory=_read_companies)
    hh_limit_per_company: int = int(os.getenv("HH_VACANCY_LIMIT_PER_COMPANY", "100"))

settings = Settings()
