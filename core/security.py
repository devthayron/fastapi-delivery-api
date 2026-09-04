from datetime import datetime, timedelta, timezone

import jwt

from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


def create_token(
    user_id: int,
    expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    jwt_type: str = "access",
):

    exp = datetime.now(timezone.utc) + expires_delta

    payload = {
        "sub": str(user_id),
        "exp": exp,
        "type": jwt_type,
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token
