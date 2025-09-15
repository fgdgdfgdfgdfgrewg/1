# HH.ru → PostgreSQL


Проект загружает работодателей и их вакансии из публичного API hh.ru в PostgreSQL, а затем предоставляет интерфейс для запросов через класс `DBManager` и простой CLI.


## Быстрый старт
1. Скопируйте `.env.example` → `.env` и заполните креды.
2. Создайте виртуальное окружение и установите зависимости:
```bash
python -m venv .venv
. .venv/bin/activate # Windows: .venv\Scripts\activate
pip install -r requirements.txt