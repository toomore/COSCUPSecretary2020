''' index '''
from models.api_token import APITokenDB
from models.subscriberdb import (SubscriberDB, SubscriberLoginTokenDB,
                                 SubscriberReadDB)

if __name__ == '__main__':
    APITokenDB().index()
    SubscriberDB().index()
    SubscriberLoginTokenDB().index()
    SubscriberReadDB().index()
