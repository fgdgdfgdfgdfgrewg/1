from __future__ import annotations
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:


    host: str = os.getenv("PG_HOST", "localhost")
port: int = int(os.getenv("PG_PORT", "5432"))
user: str = os.getenv("PG_USER", "postgres")
password: str = os.getenv("PG_PASSWORD", "postgres")
dbname: str = os.getenv("PG_DBNAME", "hh_project")

hh_base: str = os.getenv("HH_API_BASE", "https://api.hh.ru")
hh_companies: list[str] = tuple(map(str.strip, os.getenv("HH_COMPANIES", "").split(","))) if os.getenv(
    "HH_COMPANIES") else []
hh_limit_per_company: int = int(os.getenv("HH_VACANCY_LIMIT_PER_COMPANY", "100"))

settings = Settings()
