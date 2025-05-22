from dotenv import load_dotenv
import os
import base64
from passlib.context import CryptContext
from typing import Dict
from jose import jwt

HASH_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv()  # Load environment variables from .env file
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_SIGNATURE = os.getenv("JWT_SIGNATURE")
TOKEN = os.getenv("TOKEN")


class ENV:
    sheets = {
        "token": None,
        "sheets": {
            "ship_hubs": os.getenv("SHEET_SHIP_HUBS"),
            "caravan_hubs": os.getenv("SHEET_CARAVAN_HUBS")
        }
    }
    output_location = './output/'

    @staticmethod
    def encode_token(data: Dict, base_64: bool = True):
        if base_64:
            return base64.urlsafe_b64encode(
                jwt.encode(data, JWT_SIGNATURE, algorithm=JWT_ALGORITHM).encode("utf-8")
            ).decode("ascii")
        return jwt.encode(data, JWT_SIGNATURE, algorithm=JWT_ALGORITHM).encode("utf-8")

    @staticmethod
    def decode_token(token: str, base_64: bool = True):
        if base_64:
            token = base64.urlsafe_b64decode(token)

        return jwt.decode(token, JWT_SIGNATURE, algorithms=[JWT_ALGORITHM])

    @staticmethod
    def hash_given_string(given_str: str):
        return HASH_CONTEXT.hash(given_str)

    @classmethod
    def update_token(cls, new_token: str):
        data = cls.decode_token(new_token)
        cls.sheets["token"] = data


ENV.update_token(TOKEN)
