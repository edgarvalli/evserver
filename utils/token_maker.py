import jwt
from typing import Dict
from datetime import datetime, timedelta

secret_key = "p4ssw0rd"


class jwtmaker:
    @staticmethod
    def encode(payload: Dict, seconds=86400) -> str:
        payload = payload.copy()
        payload["exp"] = datetime.now() + timedelta(seconds=seconds)
        return jwt.encode(payload=payload, key=secret_key, algorithm="HS256")

    @staticmethod
    def decode(token: str) -> Dict:
        try:
            return jwt.decode(token, key=secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise {"error": True, "message": "El token ya expiro."}
        except jwt.InvalidTokenError:
            raise {"error": True, "message": "Token invalido."}
