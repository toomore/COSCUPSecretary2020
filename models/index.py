''' index '''
from models.subscriberdb import (SubscriberDB, SubscriberLoginTokenDB,
                                 SubscriberReadDB)
from models.api_token import APITokenDB

if __name__ == '__main__':
    SubscriberDB().index()
    SubscriberLoginTokenDB().index()
    SubscriberReadDB().index()

    APITokenDB().index()
