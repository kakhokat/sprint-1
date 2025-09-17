import logging
import sqlite3

import psycopg

logging.basicConfig(level=logging.INFO)

# Маппинг SQLite → PostgreSQL
TABLES = {
    "genre": {
        "sqlite_fields": [
            "model_uuid",
            "name",
            "description_text",
            "created",
            "modified",
        ],
        "pg_table": "content.genre",
        "pg_fields": [
            "genre_id",
            "name",
            "description",
            "created_at",
            "updated_at",
        ],
    },
    "person": {
        "sqlite_fields": [
            "model_uuid",
            "full_name_person",
            "created",
            "modified",
        ],
        "pg_table": "content.person",
        "pg_fields": ["person_id", "full_name", "created_at", "updated_at"],
    },
    "film_work": {
        "sqlite_fields": [
            "model_uuid",
            "title",
            "description",
            "film_type",
            "creation_date",
            "created",
            "modified",
        ],
        "pg_table": "content.film_work",
        "pg_fields": [
            "film_id",
            "title",
            "description",
            "film_type",
            "creation_date",
            "created_at",
            "updated_at",
        ],
    },
    "genre_film_work": {
        "sqlite_fields": ["model_uuid", "film_work_id", "genre_id", "created"],
        "pg_table": "content.genre_film_work",
        "pg_fields": [
            "genre_film_id",
            "film_work_id",
            "genre_id",
            "created_at",
        ],
    },
    "person_film_work": {
        "sqlite_fields": [
            "model_uuid",
            "film_work_id",
            "person_id",
            "role",
            "created",
        ],
        "pg_table": "content.person_film_work",
        "pg_fields": [
            "person_film_id",
            "film_work_id",
            "person_id",
            "role",
            "created_at",
        ],
    },
}


def load_from_sqlite(
    sqlite_conn: sqlite3.Connection, pg_conn: psycopg.Connection
):
    sqlite_cur = sqlite_conn.cursor()
    pg_cur = pg_conn.cursor()

    for table_name, cfg in TABLES.items():
        sqlite_cur.execute(
            f"SELECT {", ".join(cfg["sqlite_fields"])} FROM {table_name}"
        )
        rows = sqlite_cur.fetchall()
        if not rows:
            continue

        placeholders = ", ".join(["%s"] * len(cfg["pg_fields"]))
        pg_cur.executemany(
            f"INSERT INTO {cfg["pg_table"]} ({", ".join(cfg["pg_fields"])}) "
            f"VALUES ({placeholders}) ON CONFLICT DO NOTHING",
            rows,
        )
        logging.info(
            f"{table_name}: {len(rows)} строк перенесено в PostgreSQL."
        )

    pg_conn.commit()
    logging.info("Данные успешно перенесены из SQLite в PostgreSQL.")
