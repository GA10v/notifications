from typing import Any
from uuid import UUID

from pydantic import BaseModel


class UGCContentInfo(BaseModel):
    content_id: UUID
    user_id: UUID
    payload: Any
