import pymongo

from config import MONGODB_URI


class MongodbPipeline:

    client = None
    db = None
    collection = None

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(MONGODB_URI)
        self.db = self.client["carspass"]
        self.collection = self.db['carspass']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item.get('pined'):
            if self.collection.find_one():
                item.pop('publish_date')
                print(item.get('pined'))
        item.pop('pined', None)
        self.collection.update_one(
            filter={'id': item['id'], 'source': item['source']},
            update={'$set': item},
            upsert=True
        )
        return item
