import logging
import os
import sqlite3
from datetime import datetime
from uuid import uuid4

logging.basicConfig(level=logging.INFO)

DB_PATH = os.path.join(os.path.dirname(__file__), "db.sqlite")

# Маппинг таблиц и их полей
TABLES = {
    "genre": [
        ("model_uuid", "TEXT PRIMARY KEY"),
        ("name", "TEXT NOT NULL"),
        ("description_text", "TEXT"),
        ("created", "TEXT"),
        ("modified", "TEXT"),
    ],
    "person": [
        ("model_uuid", "TEXT PRIMARY KEY"),
        ("full_name_person", "TEXT NOT NULL"),
        ("created", "TEXT"),
        ("modified", "TEXT"),
    ],
    "film_work": [
        ("model_uuid", "TEXT PRIMARY KEY"),
        ("title", "TEXT NOT NULL"),
        ("description", "TEXT"),
        ("film_type", "TEXT NOT NULL"),
        ("creation_date", "TEXT"),
        ("created", "TEXT"),
        ("modified", "TEXT"),
    ],
    "genre_film_work": [
        ("model_uuid", "TEXT PRIMARY KEY"),
        ("film_work_id", "TEXT NOT NULL"),
        ("genre_id", "TEXT NOT NULL"),
        ("created", "TEXT"),
    ],
    "person_film_work": [
        ("model_uuid", "TEXT PRIMARY KEY"),
        ("film_work_id", "TEXT NOT NULL"),
        ("person_id", "TEXT NOT NULL"),
        ("role", "TEXT NOT NULL"),
        ("created", "TEXT"),
    ],
}

# Пример тестовых данных
NOW = datetime.now().isoformat()
GENRES = [
    (str(uuid4()), "Комедия", "Весёлый жанр", NOW, NOW),
    (str(uuid4()), "Драма", "Серьёзный жанр", NOW, NOW),
    (str(uuid4()), "Боевик", "Экшн жанр", NOW, NOW),
]

PERSONS = [
    (str(uuid4()), "Иван Иванов", NOW, NOW),
    (str(uuid4()), "Мария Петрова", NOW, NOW),
    (str(uuid4()), "Алексей Смирнов", NOW, NOW),
]

FILMS = [
    (str(uuid4()), "Фильм 1", "Описание 1", "комедия", NOW, NOW, NOW),
    (str(uuid4()), "Фильм 2", "Описание 2", "драма", NOW, NOW, NOW),
    (str(uuid4()), "Фильм 3", "Описание 3", "боевик", NOW, NOW, NOW),
]

# Связи фильм-жанр и фильм-персона
GENRE_FILM_WORK = [
    (str(uuid4()), FILMS[0][0], GENRES[0][0], NOW),
    (str(uuid4()), FILMS[1][0], GENRES[1][0], NOW),
]

PERSON_FILM_WORK = [
    (str(uuid4()), FILMS[0][0], PERSONS[0][0], "актер", NOW),
    (str(uuid4()), FILMS[1][0], PERSONS[1][0], "режиссер", NOW),
]

DATA = {
    "genre": GENRES,
    "person": PERSONS,
    "film_work": FILMS,
    "genre_film_work": GENRE_FILM_WORK,
    "person_film_work": PERSON_FILM_WORK,
}


def init_sqlite():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        logging.info("Старая SQLite база удалена.")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Создание таблиц
    for table_name, fields in TABLES.items():
        fields_sql = ", ".join(f"{name} {ftype}" for name, ftype in fields)
        cur.execute(f"CREATE TABLE {table_name} ({fields_sql})")
        logging.info(f"Таблица {table_name} создана.")

    # Вставка тестовых данных
    for table, rows in DATA.items():
        placeholders = ", ".join(["?"] * len(rows[0]))
        cur.executemany(f"INSERT INTO {table} VALUES ({placeholders})", rows)
        logging.info(
            f"В таблицу {table} вставлены данные ({len(rows)} записей)."
        )

    conn.commit()
    conn.close()
    logging.info("Инициализация SQLite с тестовыми данными завершена.")


if __name__ == "__main__":
    init_sqlite()
