import logging
import os
import sqlite3

import psycopg

from .init_sqlite import init_sqlite
from .load_data import load_from_sqlite

logging.basicConfig(level=logging.INFO)


def run_migration():
    logging.info("=== Очистка PostgreSQL ===")
    conn = psycopg.connect(
        "dbname=movies_database user=app password=123qwe "
        "host=localhost port=5432 sslmode=disable"
    )
    with conn.cursor() as cur:
        cur.execute("TRUNCATE content.person_film_work CASCADE")
        cur.execute("TRUNCATE content.genre_film_work CASCADE")
        cur.execute("TRUNCATE content.film_work CASCADE")
        cur.execute("TRUNCATE content.genre CASCADE")
        cur.execute("TRUNCATE content.person CASCADE")
        conn.commit()
    logging.info("INFO: PostgreSQL очищен.")

    logging.info("=== Создание тестовых данных SQLite ===")
    init_sqlite()

    sqlite_path = os.path.join(os.path.dirname(__file__), "db.sqlite")
    sqlite_conn = sqlite3.connect(sqlite_path)

    logging.info("\n=== Перенос данных в PostgreSQL ===")
    load_from_sqlite(sqlite_conn, conn)
    sqlite_conn.close()

    logging.info("\n=== Проверка миграции ===")
    from .check_migration import check_migration

    check_migration(conn)
    conn.close()


if __name__ == "__main__":
    run_migration()
