import sys
from typing import Any

from .db import (
    create_review_db,
    create_user_db,
    delete_user_db,
    get_movie_db,
    list_movies_db,
    list_users_db,
    update_user_db,
)

from .exceptions import MovieNotFoundError, UserNotFoundError
from fastapi import Depends, FastAPI, HTTPException, status
from .schemas import ReviewBase, UserIn
from .setup import get_connection

app = FastAPI()


# This is an endpoint, it doesn't do anything special, but it's an endpoint
@app.get("/status")
def get_status():
    return {"message": "OK"}


# list endpoints
@app.get("/movies", status_code=200)
def get_movies():
    """
    Returns a list of movies
    Unfortunately, no limit supported. sry.
    """
    con = get_connection()
    return list_movies_db(con)


@app.get("/movie/{movie_id}")
def get_movie(movie_id: int):
    con = get_connection()
    try:
        movie = get_movie_db(con, movie_id)
        return movie
    except MovieNotFoundError:
        raise HTTPException(detail="Movie not found", status_code=404)


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserIn, con: Any = Depends(get_connection)):
    result = create_user_db(con, user.username)
    if result:
        return {"message": f"User created successfully with id: {result['id']}"}
    raise HTTPException(detail="User not created properly")


@app.get("/users", status_code=200)
def get_users():
    """
    Returns a list of_users
    Unfortunately, no limit supported. sry.
    """
    con = get_connection()
    return list_users_db(con)


@app.delete("/user/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, con: Any = Depends(get_connection)):
    try:
        delete_user_db(con, user_id)
        return {"message": "User deleted"}
    except UserNotFoundError:
        raise HTTPException(
            detail="User not found", status_code=status.HTTP_404_NOT_FOUND
        )


@app.put("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_user(user_id: int, user: UserIn, con: Any = Depends(get_connection)):
    try:
        update_user_db(con, user_id, username=user.username)
        return {"message": "User deleted"}
    except UserNotFoundError:
        raise HTTPException(
            detail="User not found", status_code=status.HTTP_404_NOT_FOUND
        )


@app.post("/reviews", status_code=status.HTTP_201_CREATED)
def create_review(review: ReviewBase, con: Any = Depends(get_connection)):
    result = create_review_db(con, review)
    if result:
        return {"message": "Review created successfully", "id": result["id"]}
    raise HTTPException(detail="Review not created", status_code=400)