from datetime import date

from pydantic import BaseModel, Field


class UserIn(BaseModel):
    username: str


class ReviewBase(BaseModel):
    user_id: int
    movie_id: int
    rating: int
    review_text: str = Field(max_length=200)


class ReviewOut(BaseModel):
    rating: int
    review_text: str = Field(max_length=200)
    review_date: date
    movie_title: str
    movie_release_date: date


class UserWithReviews(BaseModel):
    id: int
    username: str
    reviews: list[ReviewOut] = []