from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class MovieType(str, Enum):
    movie = "movie"
    series = "series"
    cartoon = "cartoon"
    documentary = "documentary"


class AdminPanelContentInfo(BaseModel):
    content_id: UUID
    movie_type: MovieType
    movie_name: str
    file_path: str
