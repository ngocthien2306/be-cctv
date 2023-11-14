import pymongo

from src.utils.project_config import project_config
from src.utils.constants import DatabaseConfig

class MongoDatabase:
    def __init__(self):
        self._db_url = project_config.DB_URL
        self._client = pymongo.MongoClient(project_config.DB_URL)

        self._db = self._client[DatabaseConfig.DB_NAME]
        self._collection = self._db[DatabaseConfig.COLLECTION_NAME]

    def insert_one(self, data):
        return self._collection.insert_one(data)
    
    def delete_one(self, query):
        return self._collection.delete_one(query)
    
    def find_all(self):
        return self._collection.find()

    def get_collection(self, name: str=None):
        if name is None:
            return self._collection
        else:
            return self._db[name]

    
db_connect = MongoDatabase()

if __name__ == "__main__":
    collection = db_connect.get_collection()
    print(collection.distinct("camera_id", {"module_id": "ppe"}))
    print(collection.aggregate(
        [
        {"$match": {
            "module_id": "ppe",
            "camera_id": "camera-2"
            }
        },
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$_id",
                    },
                },
                "count": { "$sum": 1 },
            }
        }
        
        ]
    ))