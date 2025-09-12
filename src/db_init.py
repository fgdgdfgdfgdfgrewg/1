from __future__ import annotations
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pathlib import Path
from .config import settings

SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def create_database_if_needed() -> None:
    """Создаёт БД `settings.dbname`, если её ещё нет."""


conn = psycopg2.connect(host=settings.host, port=settings.port, user=settings.user, password=settings.password,
                        dbname="postgres")
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (settings.dbname,))
exists = cur.fetchone() is not None
if not exists:
    cur.execute(f"CREATE DATABASE {psycopg2.sql.Identifier(settings.dbname).string}")
cur.close()
conn.close()


def apply_schema() -> None:
    """Применяет schema.sql к целевой БД."""


with psycopg2.connect(host=settings.host, port=settings.port, user=settings.user, password=settings.password,
                      dbname=settings.dbname) as conn:
    with conn.cursor() as cur:
        sql = SCHEMA_PATH.read_text(encoding="utf-8")
        cur.execute(sql)
        conn.commit()
