from datetime import datetime, timedelta, timezone

import jwt

from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


def create_access_token(user_id: int):

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "exp": expire,
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token
