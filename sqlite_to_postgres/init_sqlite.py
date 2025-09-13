import logging
import os
import sqlite3
import uuid
from datetime import date

logging.basicConfig(level=logging.INFO)

DB_PATH = os.path.join(os.path.dirname(__file__), "db.sqlite")


def init_sqlite():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        logging.info("Старая SQLite база удалена.")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE film_work (
            film_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            creation_date TEXT,
            rating REAL,
            film_type TEXT
        )
    """
    )
    cur.execute(
        """
        CREATE TABLE genre (
            genre_id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        )
    """
    )
    cur.execute(
        """
        CREATE TABLE person (
            person_id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL
        )
    """
    )
    cur.execute(
        """
        CREATE TABLE genre_film_work (
            genre_film_id TEXT PRIMARY KEY,
            film_work_id TEXT NOT NULL,
            genre_id TEXT NOT NULL
        )
    """
    )
    cur.execute(
        """
        CREATE TABLE person_film_work (
            person_film_id TEXT PRIMARY KEY,
            film_work_id TEXT NOT NULL,
            person_id TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """
    )

    film_id = str(uuid.uuid4())
    genre_id = str(uuid.uuid4())
    person_id = str(uuid.uuid4())

    cur.execute(
        "INSERT INTO film_work VALUES (?, ?, ?, ?, ?, ?)",
        (
            film_id,
            "Inception",
            "A mind-bending thriller",
            str(date(2010, 7, 16)),
            8.8,
            "movie",
        ),
    )
    cur.execute("INSERT INTO genre VALUES (?, ?)", (genre_id, "Sci-Fi"))
    cur.execute(
        "INSERT INTO person VALUES (?, ?)", (person_id, "Leonardo DiCaprio")
    )
    cur.execute(
        "INSERT INTO genre_film_work VALUES (?, ?, ?)",
        (str(uuid.uuid4()), film_id, genre_id),
    )
    cur.execute(
        "INSERT INTO person_film_work VALUES (?, ?, ?, ?)",
        (str(uuid.uuid4()), film_id, person_id, "actor"),
    )

    conn.commit()
    conn.close()
    logging.info("SQLite база и тестовые данные созданы успешно.")


if __name__ == "__main__":
    init_sqlite()
