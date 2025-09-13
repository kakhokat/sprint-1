import logging
import sqlite3
from dataclasses import dataclass
from typing import Any, List

import psycopg

logging.basicConfig(level=logging.INFO)


@dataclass
class Film:
    film_id: str
    title: str
    description: str
    creation_date: str
    rating: float
    film_type: str


@dataclass
class Genre:
    genre_id: str
    name: str


@dataclass
class Person:
    person_id: str
    full_name: str


@dataclass
class GenreFilmWork:
    genre_film_id: str
    film_work_id: str
    genre_id: str


@dataclass
class PersonFilmWork:
    person_film_id: str
    film_work_id: str
    person_id: str
    role: str


class SQLiteLoader:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.conn.row_factory = sqlite3.Row

    def load_films(self) -> List[Film]:
        return [Film(**row) for row in self._fetch_all("film_work")]

    def load_genres(self) -> List[Genre]:
        return [Genre(**row) for row in self._fetch_all("genre")]

    def load_persons(self) -> List[Person]:
        return [Person(**row) for row in self._fetch_all("person")]

    def load_genre_film_work(self) -> List[GenreFilmWork]:
        return [
            GenreFilmWork(**row) for row in self._fetch_all("genre_film_work")
        ]

    def load_person_film_work(self) -> List[PersonFilmWork]:
        return [
            PersonFilmWork(**row)
            for row in self._fetch_all("person_film_work")
        ]

    def _fetch_all(self, table: str) -> List[dict]:
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
        return [dict(row) for row in rows]


class PostgresSaver:
    def __init__(self, conn: psycopg.Connection):
        self.conn = conn

    def save_batch(self, table: str, rows: List[Any]):
        if not rows:
            return
        columns = rows[0].__dataclass_fields__.keys()
        query = (
            f"INSERT INTO content.{table} ({", ".join(columns)}) "
            f"VALUES ({", ".join(["%s"]*len(columns))}) "
            "ON CONFLICT DO NOTHING"
        )
        try:
            with self.conn.cursor() as cur:
                for row in rows:
                    cur.execute(query, tuple(getattr(row, c) for c in columns))
            self.conn.commit()
        except Exception as e:
            logging.error("Ошибка вставки в %s: %s", table, e)
            self.conn.rollback()


def load_from_sqlite(
    sqlite_conn: sqlite3.Connection, pg_conn: psycopg.Connection
):
    loader = SQLiteLoader(sqlite_conn)
    saver = PostgresSaver(pg_conn)

    films = loader.load_films()
    genres = loader.load_genres()
    persons = loader.load_persons()
    genre_fw = loader.load_genre_film_work()
    person_fw = loader.load_person_film_work()

    logging.info(
        f"Найдено фильмов: {len(films)}"
        f"жанров: {len(genres)}"
        f"персон: {len(persons)}"
    )

    saver.save_batch("film_work", films)
    saver.save_batch("genre", genres)
    saver.save_batch("person", persons)
    saver.save_batch("genre_film_work", genre_fw)
    saver.save_batch("person_film_work", person_fw)
