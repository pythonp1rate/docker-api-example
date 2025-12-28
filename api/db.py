# db.py
import psycopg2
from .exceptions import MovieNotFoundError, UserNotFoundError
from psycopg2.extras import RealDictCursor


def get_movie_db(con, id: int):
    """
    Fetches ONE movie based on the id
    raises: MovieNotFoundError if movie was not found
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                           SELECT * FROM movies
                           WHERE id = %s
                           """,
                (id,),
            )
            result = cursor.fetchone()
            if result:
                return result
            raise MovieNotFoundError()


def list_movies_db(con):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * FROM movies;
                """
            )
            result = cursor.fetchall()
            return result


def list_users_db(con):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * FROM users;
                """
            )
            result = cursor.fetchall()
            return result


def create_user_db(con, username):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO users(username)
                VALUES(%s)
                RETURNING id
                """,
                (username,),
            )
            result = cursor.fetchone()
            if result:
                return result


def delete_user_db(con, id: int):
    """ """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                DELETE FROM users
                WHERE id = %s
                RETURNING id;
                """,
                (id,),
            )
            result = cursor.fetchone()
            if result:
                return result
            raise UserNotFoundError()


def update_user_db(con, id: int, username: str):
    """ """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE users
                SET username = %s
                WHERE id = %s
                RETURNING id;
                """,
                (username, id),
            )
            result = cursor.fetchone()
            if result:
                return result
            raise UserNotFoundError()


# We're gonna add some functions to make queries here


def get_user_with_reviews_db(con, user_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT id, username FROM users WHERE id = %s;
                """,
                (user_id,),
            )
            user = cursor.fetchone()
            if not user:
                raise UserNotFoundError()

            cursor.execute(
                """
                SELECT r.rating, r.review_text, r.review_date, m.title AS movie_title, m.release_date AS movie_release_date
                FROM reviews r
                JOIN movies m ON r.movie_id = m.id
                WHERE r.user_id = %s;
                """,
                (user_id,),
            )
            reviews = cursor.fetchall()

            # Return the user with nested reviews
            user["reviews"] = reviews
            return user


def create_review_db(con, review):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO reviews(user_id, movie_id, rating, review_text)
                VALUES(%s, %s, %s, %s)
                RETURNING id
                """,
                (review.user_id, review.movie_id, review.rating, review.review_text),
            )
            con.commit()
            return cursor.fetchone()