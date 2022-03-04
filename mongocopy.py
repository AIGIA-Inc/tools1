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


def copy(from_connection: str, to_connection: str, db: str, collection_names: List[str], window_size: int):
    with MongoClient(from_connection) as from_client:
        with MongoClient(to_connection) as to_client:
            from_db = from_client[db]
            to_db = to_client[db]
            for collection_name in collection_names:
                from_collection = from_db[collection_name]
                to_collection = to_db[collection_name]
                from_count: int = count(from_collection)
                for start in range(0, from_count, window_size):
                    copy_collection(from_collection, to_collection, start, window_size)


def drop(connection: str, db: str, collection_names: List[str]):
    with MongoClient(connection) as client:
        db = client[db]
        for collection_name in collection_names:
            collection = db[collection_name]
            collection.drop()


def counts(connection: str, db: str, collection_names: List[str]):
    result = []
    with MongoClient(connection) as client:
        db = client[db]
        for collection_name in collection_names:
            collection = db[collection_name]
            result.append(((collection_name, count(collection))))
    return result


from_connection: str = "mongodb+srv://aigreporter:33550336@cluster0.co9ud.mongodb.net/aig?retryWrites=true&w=majority"
to_connection: str   = "mongodb+srv://aigmaster:33550336@cluster0.od1kc.mongodb.net/aig?retryWrites=true&w=majority"

# from_connection: str = "mongodb+srv://aigreporter:33550336@cluster0.od1kc.mongodb.net/aig?retryWrites=true&w=majority"
# to_connection: str = "mongodb://localhost/aig"

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
    before = counts(from_connection, db_name, collections)
    drop(to_connection, db_name, collections)
    copy(from_connection, to_connection, db_name, collections, 100)
    after = counts(to_connection, db_name, collections)
    print(list(set(before) - set(after)))
