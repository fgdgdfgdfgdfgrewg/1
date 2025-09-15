from __future__ import annotations
from .db_manager import DBManager

MENU = (
    "\nВыберите действие:\n"
    "1 — Компании и количество вакансий\n"
    "2 — Все вакансии (компания | вакансия | ср.зарплата | ссылка)\n"
    "3 — Средняя зарплата по всем вакансиям\n"
    "4 — Вакансии с зарплатой выше средней\n"
    "5 — Поиск вакансий по ключевым словам\n"
    "0 — Выход\n> "
)

def run_cli() -> None:
    dbm = DBManager()
    while True:
        choice = input(MENU).strip()
        if choice == "1":
            rows = dbm.get_companies_and_vacancies_count()
            for name, cnt in rows:
                print(f"— {name}: {cnt}")
        elif choice == "2":
            rows = dbm.get_all_vacancies()
            for company, vacancy, avg, url in rows:
                avg_s = f"{avg:.0f}" if avg is not None else "—"
                print(f"— {company} | {vacancy} | {avg_s} | {url or ''}")
        elif choice == "3":
            avg = dbm.get_avg_salary()
            print(f"Средняя зарплата: {avg:.0f}" if avg is not None else "Средняя зарплата не определена")
        elif choice == "4":
            rows = dbm.get_vacancies_with_higher_salary()
            for company, vacancy, avg, url in rows:
                print(f"— {company} | {vacancy} | {avg:.0f} | {url or ''}")
        elif choice == "5":
            q = input("Введите слова через запятую: ").strip()
            keys = [x.strip() for x in q.split(",") if x.strip()]
            rows = dbm.get_vacancies_with_keyword(keys)
            for company, vacancy, avg, url in rows:
                avg_s = f"{avg:.0f}" if avg is not None else "—"
                print(f"— {company} | {vacancy} | {avg_s} | {url or ''}")
        elif choice == "0":
            print("Пока!")
            return
        else:
            print("Не понял выбор — попробуйте снова.")
