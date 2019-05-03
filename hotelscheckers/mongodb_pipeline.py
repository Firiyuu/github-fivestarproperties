import pymongo
# from scrapy.conf import settings
import settings
from bson import ObjectId
import bson



class MongoPipeline(object):
    def __init__(self):
        init_db = pymongo.MongoClient(settings.MONGODB_SERVER, settings.MONGODB_PORT)
        self.db = init_db[settings.MONGODB_DB]


    def get_collection(self):
        collection = self.db[settings.MONGODB_COLLECTION]
        return collection



