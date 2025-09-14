from __future__ import annotations
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from .config import settings

@contextmanager
def get_conn():
    conn = psycopg2.connect(
        host=settings.host,
        port=settings.port,
        user=settings.user,
        password=settings.password,
        dbname=settings.dbname,
        cursor_factory=RealDictCursor,
    )
    try:
        yield conn
    finally:
        conn.close()