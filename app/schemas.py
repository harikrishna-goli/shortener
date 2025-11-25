# SQLAlchemy models (DB tables)

from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ShortURL(Base):
    __tablename__="short_urls"
    short_code = Column(String,primary_key=True, index=True)
    long_url = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    click_count = Column(Integer, default=0)
    owner_id = Column(String, nullable=True)
    last_accessed = Column(DateTime, nullable=True)