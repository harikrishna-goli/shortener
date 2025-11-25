# DB operations (create, read, update)
# CRUD (Create , Read, Update and Delete)
from sqlalchemy.orm import Session
from app.schemas import ShortURL
from app.hashing import generate_code
from datetime import datetime



def get_long_url(db: Session, short_code: str) -> str:
    entry = db.query(ShortURL).filter_by(short_code=short_code).first()
    if not entry:
        raise ValueError("Short URL Not Found")
    entry.click_count += 1
    entry.last_accessed = datetime.now()
    db.commit()
    return entry.long_url

    
    

def create_short_url(
    db: Session,
    long_url: str,
    custom_alias: str | None = None,
    expires_at: str | None = None,
    owner_id: str | None = None
) -> str:
    try_count = 100

    if custom_alias and custom_alias.strip():
        short_code = custom_alias
        existing = db.query(ShortURL).filter_by(short_code=short_code).first()
        if existing:
            raise ValueError("Alias already exists")
    else:
        for _ in range(try_count):
            short_code = generate_code()
            existing = db.query(ShortURL).filter_by(short_code=short_code).first()
            if not existing:
                break
        else:
            raise ValueError("Unable to generate the Short URL")

    entry = ShortURL(
        short_code=short_code,
        long_url=long_url,
        expires_at=expires_at,
        click_count=0,
        owner_id=owner_id
    )
    db.add(entry)
    db.commit()
    return short_code
