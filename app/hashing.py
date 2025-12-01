# Base62 encoding / collision logic

import random
import string


# Helper: generate random short code
def generate_code(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))
