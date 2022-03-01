from pymongo import MongoClient


def count(db):
    if db:
        accounts = db.accounts
        return accounts.count({})
    else:
        raise Exception("database error")


def copy(_from, _to, skip, limit):
    if _from:
        from_accounts = _from.accounts
        to_accounts = _to.accounts
        if from_accounts and to_accounts:
            from_accounts_cursor = from_accounts.find({}).skip(skip).limit(limit)
            to_accounts.insert_many(from_accounts_cursor)
        else:
            raise Exception("collection error")
    else:
        raise Exception("database error")


from_db = "mongodb+srv://aigmaster:33550336@cluster0.od1kc.mongodb.net/aig?retryWrites=true&w=majority"
to_db = "mongodb://localhost/aig"

size = 10
with MongoClient(from_db) as from_client:
    with MongoClient(to_db) as to_client:
        from_count = count(from_client.aig)
        for start in range(0, from_count, size):
            copy(from_client.aig, to_client.aig1, start, size)
