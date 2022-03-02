from pymongo import MongoClient
from typing import List


def count(collection) -> int:
    if collection:
        return collection.count_documents({})
    else:
        raise Exception("database error")


def copy_collection(from_collection, to_collection, skip: int, limit: int):
    if from_collection and to_collection:
        from_accounts_cursor = from_collection.find({}).skip(skip).limit(limit)
        to_collection.insert_many(from_accounts_cursor)
    else:
        raise Exception("collection error")

def drop(connection: str, db: str, collections: List[str]):
    with MongoClient(connection) as client:
        db = client[db]
        for collection in collections:
            collection = db[collection]
            collection.drop()

def copy(from_connection: str, to_connection: str, db: str, collections: List[str], window_size: int):
    with MongoClient(from_connection) as from_client:
        with MongoClient(to_connection) as to_client:
            from_db = from_client[db]
            to_db = to_client[db]
            for collection in collections:
                from_collection = from_db[collection]
                to_collection = to_db[collection]
                from_count: int = count(from_collection)
                for start in range(0, from_count, window_size):
                    copy_collection(from_collection, to_collection, start, window_size)


from_connection: str = "mongodb+srv://aigmaster:33550336@cluster0.od1kc.mongodb.net/aig?retryWrites=true&w=majority"
to_connection: str = "mongodb://localhost/aig"
db_name: str = "aig"
collections: List[str] = ["accounts",
                          "articles",
                          "fs.chunks",
                          "fs.files",
                          "inquiries",
                          "nativefiles",
                          "pages",
                          "relations",
                          "sessions",
                          "shots"]

if __name__ == "__main__":
    drop(to_connection, db_name, collections)
    copy(from_connection, to_connection, db_name, collections, 100)
