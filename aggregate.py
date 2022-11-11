[
    {
        '$match': {
            'from_id': ObjectId('636b46c20e2b5ab41da72265')
        }
    }, {
        '$graphLookup': {
            'from': 'relations',
            'startWith': '$from_id',
            'connectFromField': 'from_id',
            'connectToField': 'to_id',
            'as': 'belongs',
            'maxDepth': 10,
            'depthField': 'depth',
            'restrictSearchWithMatch': {
                'type': 'belongs'
            }
        }
    }, {
        '$unwind': {
            'path': '$belongs'
        }
    }, {
        '$lookup': {
            'from': 'accounts',
            'localField': 'belongs.from_id',
            'foreignField': 'user_id',
            'as': 'account'
        }
    }, {
        '$unwind': {
            'path': '$account'
        }
    }, {
        '$addFields': {
            'account.depth': '$belongs.depth'
        }
    }, {
        '$replaceRoot': {
            'newRoot': '$account'
        }
    }, {
        '$sort': {
            'depth': -1
        }
    }, {
        '$match': {
            'type': ''
        }
    }, {
        '$project': {
            '_id': 0,
            'publickey': 0,
            'privatekey': 0,
            'secret': 0,
            'salt': 0,
            'hash': 0
        }
    }, {
        '$count': 'user_id'
    }
]