from __future__ import annotations
from typing import Iterable, List, Tuple
from .db import get_conn

class DBManager:
    """Работа с БД PostgreSQL через psycopg2."""

    def get_companies_and_vacancies_count(self) -> list[tuple[str, int]]:
        """Список компаний и количество вакансий у каждой."""
        sql = (
            """
            SELECT e.name, COUNT(v.vacancy_id)::int AS vacancies
            FROM employers e
            LEFT JOIN vacancies v USING (employer_id)
            GROUP BY e.employer_id, e.name
            ORDER BY vacancies DESC, e.name;
            """
        )
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql)  # ✅ с отступом
            rows = cur.fetchall()
            return [(r["name"], r["vacancies"]) for r in rows]

    def get_all_vacancies(self) -> List[Tuple[str, str, float | None, str | None]]:
        """Все вакансии: (компания, вакансия, средняя_зарплата, ссылка)."""
        sql = (
            """
            SELECT e.name AS company, v.name AS vacancy, v.salary_avg, v.alternate_url
            FROM vacancies v
            JOIN employers e USING (employer_id)
            ORDER BY COALESCE(v.salary_avg, 0) DESC NULLS LAST, v.published_at DESC NULLS LAST;
            """
        )
        with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
        return [(r["company"], r["vacancy"], r["salary_avg"], r["alternate_url"]) for r in rows]

    def get_avg_salary(self) -> float | None:
        """Средняя зарплата по всем вакансиям (по поддерживаемой валюте)."""
        sql = "SELECT AVG(salary_avg) AS avg_salary FROM vacancies WHERE salary_avg IS NOT NULL;"
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql)
            row = cur.fetchone()
            return float(row["avg_salary"]) if row["avg_salary"] is not None else None

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, str, float, str | None]]:
        """Вакансии, у которых зарплата выше средней по всем вакансиям."""
        sql = (
            """
            WITH avg_all AS (
                SELECT AVG(salary_avg) AS a FROM vacancies WHERE salary_avg IS NOT NULL
            )
            SELECT e.name AS company, v.name AS vacancy, v.salary_avg, v.alternate_url
            FROM vacancies v
            JOIN employers e USING (employer_id)
            CROSS JOIN avg_all
            WHERE v.salary_avg IS NOT NULL AND v.salary_avg > avg_all.a
            ORDER BY v.salary_avg DESC;
            """
        )
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            return [(r["company"], r["vacancy"], r["salary_avg"], r["alternate_url"]) for r in rows]

    def get_vacancies_with_keyword(self, *keywords: Iterable[str]) -> List[Tuple[str, str, float | None, str | None]]:
        """Вакансии, в названии которых содержатся переданные слова (ILIKE)."""
        flat = [k for ks in keywords for k in (ks if isinstance(ks, (list, tuple, set)) else [ks])]
        flat = [k.strip() for k in flat if k and str(k).strip()]
        if not flat:
            return []
        like = " OR ".join([f"v.name ILIKE %s" for _ in flat])
        sql = (
            f"""
            SELECT e.name AS company, v.name AS vacancy, v.salary_avg, v.alternate_url
            FROM vacancies v
            JOIN employers e USING (employer_id)
            WHERE {like}
            ORDER BY v.published_at DESC NULLS LAST;
            """
        )
        params = [f"%{k}%" for k in flat]
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            return [(r["company"], r["vacancy"], r["salary_avg"], r["alternate_url"]) for r in rows]