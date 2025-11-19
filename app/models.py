# Pydantic models (request/response schemas)
from pydantic import BaseModel


# Request model (input JSON for /shorten)
class URLRequest(BaseModel):
    owner_id: str
    long_url: str
    custom_alias: str | None = None
    expires_at: str | None = None

# Response model (output JSON for /shorten)
class URLResponse(BaseModel):
    short_url: str
    owner_id: str
    expires_at: str | None = None
    message: str