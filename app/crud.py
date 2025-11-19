# DB operations (create, read, update)
# CRUD (Create , Read, Update and Delete)
from app.hashing import generate_code

url_map = {}


def get_long_url(short_code: str) -> str:
    if short_code not in url_map:
        raise ValueError("Short URL Not Found")
    entry = url_map[short_code]
    entry["click_count"] += 1
    return entry["long_url"]
    
    

def create_short_url(owner_id: str,long_url: str, custom_alias: str | None = None, expires_at: str | None = None) -> str:
    try_count = 100
    if custom_alias is not None:
        short_code = custom_alias
        if short_code in url_map:
            raise ValueError("Alias already exists")
    else:
        for index in range(try_count):
            short_code = generate_code()
            if short_code not in url_map:
                break
        else:
            raise ValueError("Unable to generate the Short URL")
    url_map[short_code] = {"long_url" : long_url,
                           "expires_at" : expires_at,
                            "click_count":0,
                            "owner_id": owner_id}
    return short_code