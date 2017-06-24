from pymongo.mongo_client import MongoClient


class StorageEngine(object):

    def __init__(self, config):
        user = config['db']['user']
        password = config['db']['password']
        host = config['db']['host']
        database = config['db']['database']
        uri = "mongodb://{0}:{1}@{2}".format(
            user, password, host)
        client = MongoClient(uri)
        self.db = client[database]

    def serialize_datetime(self, data):
        key_list = ['createdDate', 'lastModifiedDate', 'DeletedDate', 'timeStamp']
        for key in key_list:
            if data.get(key):
                data[key] = str(data[key])


    def search_by_condition(self, collection, condition):
        try:
            result = self.db[collection].find(condition)
        except Exception as ex:
            return ex
        else:
            result_list = list()
            for item in result:
                item['id'] = str(item.pop('_id'))
                self.serialize_datetime(item)
                result_list.append(item)
            return result_list
