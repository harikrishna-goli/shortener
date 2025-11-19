from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from app.models import URLRequest, URLResponse
from app.hashing import generate_code
from app.crud import get_long_url, create_short_url

app = FastAPI()


#Post to create an short name and return it
@app.post("/shorten", response_model=URLResponse)
def shorten_url(request: URLRequest):
    try:
        short_code = create_short_url(request.owner_id, request.long_url, request.custom_alias, request.expires_at)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return URLResponse(
        short_url = f"http://127.0.0.1:8000/{short_code}",
        expires_at = request.expires_at,
        owner_id = request.owner_id,
        message = "Short URL created successfully"
    )

#Get to redirect to orginal url
@app.get("/{short_code}")
def redirect(short_code: str):
    try:
        long_url = get_long_url(short_code)
    except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))
    return RedirectResponse(url=long_url)
