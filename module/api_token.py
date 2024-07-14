from typing import Any
from uuid import uuid4
from dataclasses import dataclass, asdict, field

from passlib.context import CryptContext # type: ignore

from models.api_token import APITokenDB

@dataclass
class APITokenSchema:
    token: str = field(default_factory=lambda: uuid4().hex)
    serial_no: str = field(default_factory=lambda: f'{uuid4().node:08x}')
    label: str = ''

class APIToken:
    @staticmethod
    def create(label: str) -> APITokenSchema:
        new_token = APITokenSchema(label=label)

        hash_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        hashed_token = asdict(new_token)
        hashed_token['token'] = hash_context.hash(hashed_token['token'])
        
        APITokenDB().insert_one(hashed_token)

        new_token.token = f'{new_token.serial_no}|{new_token.token}'

        return new_token
    
    @staticmethod
    def get_list() -> list[dict[str, Any]]:
        return list(APITokenDB().find({}, { 'label': 1, 'serial_no': 1, '_id': 0 }))
    
    @staticmethod
    def delete(tokens: list[str]) -> None:
        APITokenDB().delete_many({
            'serial_no': { '$in': tokens }
        })

    @staticmethod
    def verify(token: str) -> bool:
        schema, token = token.split(' ')
        if schema.lower() != 'bearer':
            return False
        
        serial_no, token = token.split('|')
        hash_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        hashed_token = APITokenDB().find_one({
            'serial_no': serial_no
        })

        return hash_context.verify(token, hashed_token['token']) # type: ignore
