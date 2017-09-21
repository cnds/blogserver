import logging

from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId


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
        key_list = [
            'createdDate', 'lastModifiedDate', 'DeletedDate', 'timeStamp'
        ]
        for key in key_list:
            if data.get(key):
                data[key] = str(data[key])

    def transform_to_object_id(self, object_id):
        try:
            validated_id = ObjectId(object_id)
        except InvalidId as ex:
            return False, ex
        else:
            return True, validated_id


    def search_by_condition(self, collection, condition):
        try:
            result = self.db[collection].find(condition)
        except Exception as ex:
            return False, ex
        else:
            result_list = list()
            for item in result:
                item['id'] = str(item.pop('_id'))
                self.serialize_datetime(item)
                result_list.append(item)
            return True, result_list

    def create(self, collection, data):
        try:
            result = self.db[collection].insert_one(data)
        except Exception:
            return False
        else:
            return {'id': str(result.inserted_id)}

    def update_by_id(self, collection, object_id, data):
        flag, validated_id = self.transform_to_object_id(object_id)
        if not flag:
            logging.error(validated_id)
            return False

        try:
            self.db[collection].update_one({'_id': validated_id},
                                           {'$set': data})
        except Exception as ex:
            logging.error('update error: %s' % ex)
            return False
        else:
            return {'id': object_id}

    def search_by_id(self, collection, object_id):
        flag, validated_id = self.transform_to_object_id(object_id)
        if not flag:
            return False, validated_id

        result = self.db[collection].find_one({'_id': validated_id})
        if result:
            result['id'] = str(result.pop('_id'))
            self.serialize_datetime(result)
            return True, result
        else:
            return False, None

    def remove_by_id(self, collection, object_id):
        flag, validated_id = self.transform_to_object_id(object_id)
        if not flag:
            logging.error(validated_id)
            return False

        try:
            self.db[collection].remove({'_id': validated_id})
        except Exception as ex:
            logging.error('remove error: %s' % ex)
            return False
        else:
            return {'id': object_id}
