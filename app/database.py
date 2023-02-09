from os import getenv
from typing import Dict

from pymongo import MongoClient
from dotenv import load_dotenv
from pymongo.cursor import Cursor


class MongoDB:
    load_dotenv()
    collection = MongoClient(getenv("URL"))["ThisNotTwitterWS"]["TheseNotTweetsWS"]

    def count(self):
        return self.collection.count_documents({})

    def find_all(self) -> Cursor[Dict]:
        return self.collection.find({}, {"_id": False})

    def insert_one(self, payload: Dict) -> bool:
        payload["id"] = self.count()
        return self.collection.insert_one(payload).acknowledged
