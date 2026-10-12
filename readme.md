# Hotel Booking Persistence Layer

Лабораторна робота №7 з дисципліни «Професійний Python»

## Опис проєкту

Проєкт демонструє організацію шару зберігання даних (persistence layer) для системи бронювання готелю (Варіант 8) з використанням реляційної СУБД SQLite, стандарту Python DB-API та SQLAlchemy ORM.
У межах роботи реалізовано:
- **База даних та ORM-моделі:** Створення таблиць (Rooms, Guests, Reservations) із застосуванням PRIMARY KEY, FOREIGN KEY, та UNIQUE/CHECK constraints.
- **Python DB-API та Parameterized queries:** Захист від SQL-ін'єкцій при виконанні сирих SQL-запитів.
- **Repository Pattern та Unit of Work:** Відокремлення бізнес-логіки від доступу до даних, використання Generic Repository (із пагінацією та сортуванням) та керування транзакціями (ізоляція `commit` та `rollback`).
- **Транзакції та принципи ACID:** Надійне бронювання номерів із перевіркою конфліктів дат та автоматичним відкочуванням змін при помилках.
- **Агрегації та складні JOIN:** Використання SQL-функцій `SUM()`, `GROUP BY` для підрахунку виручки та історії бронювань.
- **Міграції баз даних (Alembic):** Автоматизоване оновлення схеми бази даних (додавання поля `phone_number` до таблиці `guests`).
- **Integration Tests:** Тестування бази даних із використанням ізольованої in-memory БД SQLite.

## Структура проєкту (src-layout)

```text
hotel_booking/
│
├── pyproject.toml
├── alembic.ini            # Налаштування міграцій Alembic
├── hotel.db               # Файл бази даних SQLite (генерується)
├── README.md
├── migrations/            # Папка міграцій (Alembic)
│   ├── env.py
│   └── versions/
│
├── src/
│   └── hotel_booking/
│       ├── __init__.py
│       ├── database.py    # Налаштування engine та DB-API
│       ├── models.py      # SQLAlchemy ORM моделі
│       ├── repositories.py# Generic та специфічні репозиторії
│       ├── uow.py         # Unit of Work для транзакцій
│       ├── services.py    # Бізнес-логіка (бронювання, агрегації)
│       └── main.py        # Точка входу
│
└── tests/
    ├── conftest.py        # Fixtures та налаштування in-memory DB
    └── test_hotel.py      # Інтеграційні тести (CRUD, Rollback, Constraints)
```

## Вимоги

- Python 3.14+
- uv (система керування залежностями)
- sqlalchemy, alembic, pytest, pytest-cov

## Встановлення та запуск

1. Встановлення залежностей через `uv`:

```bash
uv sync
```

2. Застосування міграцій бази даних (створення таблиць та оновлення схеми):

```bash
uv run alembic upgrade head
```

3. Запуск головного скрипта застосунку (демонстрація CRUD та транзакцій):

```bash
uv run python -m hotel_booking.main
```

4. Запуск інтеграційних тестів:

```bash
uv run pytest -v
```

## Результати тестування

Комплекс інтеграційних тестів перевіряє `Create`, `Read`, `Update`, `Delete` операції, дотримання CHECK констрейнтів бази даних (заборона від'ємної ціни), а також коректність транзакцій. Особлива увага приділена перевірці `rollback` операцій при спробі подвійного бронювання одного номера на ті ж дати, що гарантує цілісність даних (Consistency).

## Автор

Студент: Івасів Данило  
Група: ФеП-32  
Викладач: доц. Куньо І. М.