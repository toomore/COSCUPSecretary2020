''' API Token Module '''
from typing import Any
from uuid import uuid4
from dataclasses import dataclass, asdict, field

from passlib.context import CryptContext

from models.api_token import APITokenDB

@dataclass
class APITokenSchema:
    ''' Schema of api_token collection '''
    token: str = field(default_factory=lambda: uuid4().hex)
    serial_no: str = field(default_factory=lambda: f'{uuid4().node:08x}')
    label: str = ''

class APIToken:
    ''' Class for managing API tokens '''
    @staticmethod
    def create(label: str) -> APITokenSchema:
        ''' Create token '''
        new_token = APITokenSchema(label=label)

        hash_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        hashed_token = asdict(new_token)
        hashed_token['token'] = hash_context.hash(hashed_token['token'])

        APITokenDB().insert_one(hashed_token)

        new_token.token = f'{new_token.serial_no}|{new_token.token}'

        return new_token

    @staticmethod
    def get_list() -> list[dict[str, Any]]:
        ''' Get list of token '''
        return list(APITokenDB().find({}, { 'label': 1, 'serial_no': 1, '_id': 0 }))

    @staticmethod
    def delete(tokens: list[str]) -> None:
        ''' Delete the given token serial_no '''
        APITokenDB().delete_many({
            'serial_no': { '$in': tokens }
        })

    @staticmethod
    def verify(token: str) -> bool:
        ''' Check if the token exists and valid '''
        schema, token = token.split(' ')
        if schema.lower() != 'bearer':
            return False

        serial_no, token = token.split('|')
        hash_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        hashed_token = APITokenDB().find_one({
            'serial_no': serial_no
        })

        if hashed_token is None:
            return False

        return hash_context.verify(token, hashed_token['token'])
