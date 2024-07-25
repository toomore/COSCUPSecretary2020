''' APIToken DB '''
from models.base import DBBase

class APITokenDB(DBBase):
    ''' Token Collection

    Schema:
    {
        serial_no: string,
        token: string,
        label: string
    }
    '''
    def __init__(self) -> None:
        super().__init__('api_token')

    def index(self) -> None:
        ''' index '''
        self.create_index([('serial_no', 1)])
