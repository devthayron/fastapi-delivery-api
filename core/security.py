from datetime import datetime, timedelta, timezone

import jwt

from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


def create_token(
    user_id: int,
    expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
):

    exp = datetime.now(timezone.utc) + expires_delta

    payload = {
        "sub": str(user_id),
        "exp": exp,
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token
