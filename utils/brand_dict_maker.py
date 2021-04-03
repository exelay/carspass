import json

import pymongo


client = pymongo.MongoClient(
    "mongodb+srv://imdb:rowdy0987@carspass.mskrx.mongodb.net/<dbname>?retryWrites=true&w=majority"
)
db = client["Carspass"]
collection = db['carspass']

brands_data = dict()


def collect_brands_data():
    print("Start collecting brands data")

    for doc in collection.find():
        brand = doc["brand"]
        model = doc["model"]
        if brands_data.get(brand):
            brands_data[brand].add(model)
        else:
            brands_data[brand] = set()
            brands_data[brand].add(model)

    print("Data collecting finished!")


def write_brands_data():
    for brand in brands_data.keys():
        models = brands_data[brand]
        brands_data[brand] = list(models)
    with open("brands_data.json", "w") as file:
        json.dump(brands_data, file, ensure_ascii=False)


if __name__ == '__main__':
    collect_brands_data()
    write_brands_data()
