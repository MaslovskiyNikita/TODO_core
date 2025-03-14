from datetime import datetime, timedelta

import jwt


class JWTGenerator:

    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def jwt_code(self, payload: dict, expiration_days: int = 1) -> str:

        payload["exp"] = datetime.now() + timedelta(days=expiration_days)
        token = jwt.encode(payload, self.secret_key, self.algorithm)

        return token
