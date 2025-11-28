#SQLAlchemy ORM classes (tables)

from sqlalchemy import Column, String, Integer, DateTime
from app.database import Base

class ShortURL(Base):
    __tablename__ = "short_urls"
    short_code = Column(String(10), primary_key=True)
    long_url = Column(String(2048), nullable=False)
    expires_at = Column(DateTime, nullable=True)
    click_count = Column(Integer, default=0, nullable=False)
    owner_id = Column(String(64), nullable=True)
    last_accessed = Column(DateTime, nullable=True)
