from __future__ import annotations
from typing import Sequence
from psycopg2.extras import execute_values
from .db import get_conn
from .utils.salary import calc_salary_avg

def upsert_employers(employers: Sequence[dict]) -> None:
    rows = []
    for e in employers:
        rows.append((
            int(e["id"]),
            e.get("name"),
            e.get("url"),
            e.get("alternate_url"),
            e.get("vacancies_url"),
            bool(e.get("trusted")),
        ))
    sql = (
        """
        INSERT INTO employers (employer_id, name, url, alternate_url, vacancies_url, trusted)
        VALUES %s
        ON CONFLICT (employer_id) DO UPDATE
          SET name = EXCLUDED.name,
              url = EXCLUDED.url,
              alternate_url = EXCLUDED.alternate_url,
              vacancies_url = EXCLUDED.vacancies_url,
              trusted = EXCLUDED.trusted;
        """
    )
    with get_conn() as conn:
        with conn.cursor() as cur:
            if rows:
                execute_values(cur, sql, rows)
        conn.commit()

def upsert_vacancies(vacancies: Sequence[dict]) -> None:
    rows = []
    for v in vacancies:
        currency, s_from, s_to, s_avg = calc_salary_avg(v.get("salary"))
        rows.append((
            int(v["id"]),
            int(v["employer"]["id"]),
            v.get("name"),
            (v.get("area") or {}).get("name"),
            v.get("published_at"),
            v.get("alternate_url"),
            currency,
            s_from,
            s_to,
            s_avg,
            (v.get("snippet") or {}).get("requirement"),
            (v.get("snippet") or {}).get("responsibility"),
        ))
    sql = (
        """
        INSERT INTO vacancies (
            vacancy_id, employer_id, name, area_name, published_at, alternate_url, currency,
            salary_from, salary_to, salary_avg, requirement_snip, responsibility_snip
        ) VALUES %s
        ON CONFLICT (vacancy_id) DO UPDATE SET
            employer_id = EXCLUDED.employer_id,
            name = EXCLUDED.name,
            area_name = EXCLUDED.area_name,
            published_at = EXCLUDED.published_at,
            alternate_url = EXCLUDED.alternate_url,
            currency = EXCLUDED.currency,
            salary_from = EXCLUDED.salary_from,
            salary_to = EXCLUDED.salary_to,
            salary_avg = EXCLUDED.salary_avg,
            requirement_snip = EXCLUDED.requirement_snip,
            responsibility_snip = EXCLUDED.responsibility_snip;
        """
    )
    with get_conn() as conn:
        with conn.cursor() as cur:
            if rows:
                execute_values(cur, sql, rows)
        conn.commit()