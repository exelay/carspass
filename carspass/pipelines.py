import pymongo
from itemadapter import ItemAdapter


class MongodbPipeline:

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(
            "mongodb+srv://imdb:rowdy0987@carspass.mskrx.mongodb.net/<dbname>?retryWrites=true&w=majority"
        )
        self.db = self.client["IMDB"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = spider.token
        self.db[collection_name].insert_one(ItemAdapter(item).asdict())
        return item
