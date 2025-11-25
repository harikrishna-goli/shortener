# Pydantic models (request/response schemas)
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Request model (input JSON for /shorten)
class URLRequest(BaseModel):
    owner_id: str | None = None
    long_url: str
    custom_alias: str | None = None
    expires_at: Optional[datetime] = None

# Response model (output JSON for /shorten)
class URLResponse(BaseModel):
    short_url: str
    short_code: str
    owner_id: Optional[str] = None
    expires_at: Optional[datetime] = None
    message: str