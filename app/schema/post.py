from pydantic import BaseModel , Field

from datetime import datetime


class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    published: bool = False


class PostUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )

    content: str | None = Field(
        default=None,
        min_length=1,
    )

    published: bool | None = None


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    author_id: int
    created_at: datetime
    updated_at: datetime