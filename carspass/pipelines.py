import pymongo


class MongodbPipeline:

    client = None
    db = None
    collection = None

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(
            "mongodb+srv://imdb:rowdy0987@carspass.mskrx.mongodb.net/<dbname>?retryWrites=true&w=majority"
        )
        self.db = self.client["Carspass"]
        self.collection = self.db[spider.scraping_time]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = spider.scraping_time
        if not self.collection.count_documents({'id': item['id']}):
            self.db[collection_name].insert_one(item)
        return item
