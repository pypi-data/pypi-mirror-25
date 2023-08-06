import json
from datetime import datetime

from bson import Timestamp
from bson.objectid import ObjectId


class MongoDBEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Timestamp):
            dt = datetime.fromtimestamp(obj.time)
            return dt.strftime('%Y-%m-%dT%H:%M:%SZ')

        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')

        if isinstance(obj, ObjectId):
            return repr(ObjectId)

        return super().default(obj)
