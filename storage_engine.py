from pymongo.mongo_client import MongoClient
from urllib.parse import quote_plus


user = 'admin'
password = '123456'
host = 'rd.dacdy.xyz'
uri = "mongodb://{0}:{1}@{2}".format(quote_plus(user),
                                     quote_plus(password),
                                     host)
client = MongoClient(uri)

db = client['authorization']
