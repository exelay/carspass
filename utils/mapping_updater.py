import json

import pymongo

from config import MONGODB_URI


sites = ('avito', 'amru', 'drom', 'autoru')


class MappingUpdater:
    client = pymongo.MongoClient(MONGODB_URI)
    db = client["carspass"]
    collection = db['carspass']
    dictionaries_path = '/Users/exelay/Documents/Projects/Work/carspass/dictionaries'

    def __init__(self, site):
        self.site = site
        with open(f'{self.dictionaries_path}/map.{site}.json', 'r', encoding='utf-8') as f:
            self.mapping = json.load(f)

    def update_brand(self, _id, brand):
        self.collection.update_one(
            filter={'_id': _id},
            update={'$set': {'source_brand': brand}}
        )
        try:
            new_brand = self.mapping[brand][0]
            if brand != new_brand:
                print(f"{brand} >>> {new_brand}")
                self.collection.update_one(
                    filter={'_id': _id},
                    update={'$set': {'brand': new_brand}}
                )
        except KeyError:
            pass
        except Exception as e:
            print(e)

    def update_model(self, _id, brand, model):
        self.collection.update_one(
            filter={'_id': _id},
            update={'$set': {'source_model': model}}
        )
        try:
            new_model = self.mapping[brand][1][model]
            if model != new_model:
                print(f"{brand} - {model} >>> {brand} - {new_model}")
                self.collection.update_one(
                    filter={'_id': _id},
                    update={'$set': {'model': new_model}}
                )
        except KeyError:
            pass
        except Exception as e:
            print(e)

    def update_items(self):
        print(f"|-------|{self.site}|--------|")
        for item in self.collection.find({'source': self.site}, no_cursor_timeout=True):
            _id = item['_id']
            brand = item['brand']
            model = item['model']
            self.update_brand(_id, brand)
            self.update_model(_id, brand, model)


if __name__ == '__main__':
    for site in sites:
        updater = MappingUpdater(site)
        updater.update_items()

