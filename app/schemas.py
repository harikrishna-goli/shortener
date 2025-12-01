# Pydantic request/response classes.
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class URLRequest(BaseModel):
    owner_id: Optional[str] = None
    long_url: str
    custom_alias: Optional[str] = None
    expires_at: Optional[datetime] = None


class URLResponse(BaseModel):
    short_url: str
    short_code: str
    owner_id: Optional[str] = None
    expires_at: Optional[datetime] = None
    message: str
