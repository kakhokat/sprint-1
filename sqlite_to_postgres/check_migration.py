import logging

import psycopg

logging.basicConfig(level=logging.INFO)

TABLES = [
    "film_work",
    "genre",
    "person",
    "genre_film_work",
    "person_film_work",
]


def check_migration(pg_conn: psycopg.Connection):
    with pg_conn.cursor() as cur:
        for table in TABLES:
            cur.execute(f"SELECT COUNT(*) FROM content.{table}")
            count = cur.fetchone()[0]
            logging.info(f"{table}: {count} rows")

        logging.info("\nСвязи фильм-жанр:")
        cur.execute("SELECT * FROM content.genre_film_work")
        for row in cur.fetchall():
            logging.info(row)

        logging.info("\nСвязи фильм-персона:")
        cur.execute("SELECT * FROM content.person_film_work")
        for row in cur.fetchall():
            logging.info(row)
