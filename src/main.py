from src.config import settings
from src import db_init
from src.hh_api import search_employers_by_name, iter_vacancies_by_employer
from src.loader import upsert_employers, upsert_vacancies
from src.cli import run_cli

def bootstrap() -> None:
    # 1) Создать БД и схему
    db_init.create_database_if_needed()
    db_init.apply_schema()

    # 2) Найти 10+ работодателей
    employers = search_employers_by_name(settings.hh_companies)
    if len(employers) < 10:
        print("⚠️ Найдено меньше 10 работодателей. Проверьте список HH_COMPANIES в .env")
    upsert_employers(employers)

    # 3) Загрузить вакансии по каждому работодателю
    all_vacancies = []
    for e in employers:
        eid = int(e["id"])
        for v in iter_vacancies_by_employer(eid, settings.hh_limit_per_company):
            all_vacancies.append(v)
    upsert_vacancies(all_vacancies)

if __name__ == "__main__":
    bootstrap()
    run_cli()
