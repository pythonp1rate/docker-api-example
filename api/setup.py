import os

import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_NAME = os.getenv("DATABASE")
PASSWORD = os.getenv("PASSWORD")


def get_connection():
    return psycopg2.connect(
        dbname=DATABASE_NAME,
        user="postgres",  # change if needed
        password=PASSWORD,
        host=os.getenv("DB_HOST", "localhost"),  # Use the DB_HOST variable
        port=os.getenv("DB_PORT", "5432"),  # Use the DB_PORT variable
    )


def create_tables():
    con = get_connection()
    create_user_table_query = """ CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE
    )
    """

    create_genre_table_query = """
    CREATE TABLE IF NOT EXISTS genres(
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE
    )
    """

    create_movies_table_query = """
    CREATE TABLE IF NOT EXISTS movies(
        id SERIAL PRIMARY KEY,
        title VARCHAR(200) UNIQUE,
        release_date DATE,
        genre_id INT REFERENCES genres(id)
    )
    """

    watchlist = """
    CREATE TABLE IF NOT EXISTS watchlist(
        user_id INT REFERENCES users(id),
        movie_id INT REFERENCES movies(id),
        added_date DATE DEFAULT CURRENT_DATE,
        PRIMARY KEY(user_id, movie_id)
    )
    """

    reviews = """
    CREATE TABLE IF NOT EXISTS reviews(
        id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(id),
        movie_id INT REFERENCES movies(id),
        rating INT,
        review_text TEXT,
        review_date DATE DEFAULT CURRENT_DATE
    )
    """

    with con:
        with con.cursor() as cursor:
            cursor.execute(create_user_table_query)
            cursor.execute(create_genre_table_query)
            cursor.execute(create_movies_table_query)
            cursor.execute(reviews)
            cursor.execute(watchlist)


def seed_data():
    """Seed the database with sample data."""
    con = get_connection()

    genres = [
        ("Action",),
        ("Comedy",),
        ("Drama",),
        ("Science Fiction",),
        ("Horror",),
        ("Romance",),
    ]

    movies = [
        ("The Matrix", "1999-03-31", 4),  # Science Fiction
        ("Die Hard", "1988-07-15", 1),  # Action
        ("The Shawshank Redemption", "1994-09-23", 3),  # Drama
        ("Superbad", "2007-08-17", 2),  # Comedy
        ("The Conjuring", "2013-07-19", 5),  # Horror
        ("Titanic", "1997-12-19", 6),  # Romance
        ("Inception", "2010-07-16", 4),  # Science Fiction
        ("Gladiator", "2000-05-05", 1),  # Action
    ]

    users = [
        ("alice",),
        ("bob",),
        ("charlie",),
    ]

    reviews = [
        (1, 1, 5, "Mind-blowing movie!"),  # alice reviews The Matrix
        (1, 3, 5, "A masterpiece."),  # alice reviews Shawshank
        (2, 1, 4, "Great action scenes."),  # bob reviews The Matrix
        (2, 4, 3, "Pretty funny."),  # bob reviews Superbad
        (3, 7, 5, "Nolan is a genius."),  # charlie reviews Inception
    ]

    with con:
        with con.cursor() as cursor:
            # Insert genres
            cursor.executemany(
                "INSERT INTO genres(name) VALUES(%s) ON CONFLICT (name) DO NOTHING",
                genres
            )

            # Insert movies
            cursor.executemany(
                """INSERT INTO movies(title, release_date, genre_id)
                    VALUES(%s, %s, %s) ON CONFLICT (title) DO NOTHING""",
                movies
            )

            # Insert users
            cursor.executemany(
                "INSERT INTO users(username) VALUES(%s) ON CONFLICT (username) DO NOTHING",
                users
            )

            # Insert reviews
            for review in reviews:
                cursor.execute(
                    """INSERT INTO reviews(user_id, movie_id, rating, review_text)
                        VALUES(%s, %s, %s, %s)
                        ON CONFLICT DO NOTHING""",
                    review
                )


if __name__ == "__main__":
    # Only reason to execute this file would be to create new tables, meaning it serves a migration file
    create_tables()
    print("Tables created successfully.")
    seed_data()
    print("Sample data seeded successfully.")