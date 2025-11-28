from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.models import URLRequest, URLResponse
from app.crud import get_long_url, create_short_url
from app.database import get_db
from app.schemas import ShortURL



app = FastAPI()

#POST to create an short name and return it
@app.post("/shorten", response_model=URLResponse)
def shorten_url(request: URLRequest, db: Session = Depends(get_db)):
    try:
        short_code = create_short_url(
            db, 
            request.long_url, 
            request.custom_alias, 
            request.expires_at,
            request.owner_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return URLResponse(
        short_url = f"http://127.0.0.1:8000/{short_code}",
        short_code = short_code,
        expires_at = request.expires_at,
        owner_id = request.owner_id,
        message = "Short URL created successfully"
    )

#Get to redirect to orginal url
@app.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):
    try:
        long_url = get_long_url(db, short_code)
    except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))
    return RedirectResponse(url=long_url)


@app.get("/stats/{short_code}")
def status_page(short_code: str, db: Session = Depends(get_db)):

    table = db.query(ShortURL).filter_by(short_code = short_code).first()
    if table is None:
        raise HTTPException(status_code=404, detail="Stats not found")
    
    
    return {
        "short_code" : table.short_code,
        "long_url" : table.long_url,
        "expires_at" : table.expires_at,
        "click_count" : table.click_count,
        "owner_id" : table.owner_id,
        "last_accessed": table.last_accessed
    }

