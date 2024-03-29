#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pm2登録
# pm2 start main.py --name reporter --interpreter python3

import os
import json
import pathlib

from typing import Any
from datetime import datetime
import time

import uvicorn
from bson import ObjectId

from pymongo import MongoClient
import pandas as pd

from fastapi import (
    FastAPI,
    APIRouter,
    Request
)
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional

import requests

app = FastAPI()

PATH_ROOT = str(pathlib.Path(__file__).resolve().parent)
PATH_TEMPLATES = str(pathlib.Path(__file__).resolve().parent / "templates")
PATH_STATIC = str(pathlib.Path(__file__).resolve().parent / "static")

app.mount("/static", StaticFiles(directory=PATH_STATIC), name="static")
templates = Jinja2Templates(directory=PATH_TEMPLATES)

import logging


# logger = logging.getLogger('uvicorn')
# logger.info('info-test')


# app.logger.setLevel(logging.DEBUG)

# log_path = os.path.expanduser(os.path.join("../logs", "tools.log"))
# log_handler = logging.FileHandler(log_path)
# log_handler.setLevel(logging.DEBUG)
# app.logger.addHandler(log_handler)
# root_path = "../public/result"
# default_root_user = "admin@aigia.co.jp"

def sister(name):
    return os.path.expanduser(os.path.join(PATH_ROOT, name))


def config():
    json_open = open('config/default.json', 'r')
    json_load = json.load(json_open)

    host = json_load['host']
    path = json_load['path']
    key = json_load['key']
    username = json_load['username']
    password = json_load['password']
    return host, path, key, username, password


def stripe_config():
    json_open = open('config/default.json', 'r')
    json_load = json.load(json_open)
    stripe = json_load['stripe']
    return stripe


def connect_string(protocol, username, password, host, db):
    #return "mongodb://localhost/aig"
    return protocol + "://" + username + ":" + password + "@" + host + "/" + db


@app.get('/')
def index(request: Request, key: str = "", root: str = "admin@aigia.co.jp", layout: str = "fdp"):
    host, path, _key, username, password = config()
    return templates.TemplateResponse("index.j2",
                                      context={"request": request, "host": host, "path": path, "key": _key,
                                               "rootuser": root, "layout": layout})


"""
@app.get('/tree')
def tree(request: Request, key: str = "", root: str = "admin@aigia.co.jp"):
    from aig_accounts import accounts
    host, path, _key, username, password = config()
    with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                    "aig?retryWrites=true&w=majority")) as client:
        _accounts = accounts.relation_tree(client.aig, root)
    return templates.TemplateResponse("accounts_tree.j2",
                                      context={"request": request, "host": host, "path": path, "key": key,
                                               "rootuser": root, "accounts": _accounts})
"""


@app.get('/accounts')
def accounts(request: Request, key: str = "", root: str = "admin@aigia.co.jp"):
    host, path, _key, username, password = config()

    try:
        return templates.TemplateResponse("accounts.j2",
                                          context={"request": request, "host": host, "path": path, "key": key,
                                                   "rootuser": root})
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


def json_serial(user):
    date = user['date']
    if isinstance(date, (datetime, date)):
        user['date'] = date.isoformat()
    return user


@app.get('/api/accounts')
def api_accounts(key: str = "", skip: int = 0, limit: int = 20, category: str = ""):
    from aig_accounts import accounts, payment

    host, path, _key, username, password = config()

    try:
        stripeconfig = stripe_config()
        stripe = payment.Stripe(stripeconfig['protocol'], stripeconfig['host'], stripeconfig['key'])
        with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                        "aig?retryWrites=true&w=majority")) as client:
            users = accounts.accounts(client.aig, skip, limit, stripe, category)
        return JSONResponse(content=list(map(json_serial, users)))
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@app.get('/api/accounts/count')
def api_accounts(key: str = "", skip: int = 0, category: str = ""):
    from aig_accounts import accounts, payment
    host, path, _key, username, password = config()

    try:
        stripeconfig = stripe_config()
        stripe = payment.Stripe(stripeconfig['protocol'], stripeconfig['host'], stripeconfig['key'])
        with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                        "aig?retryWrites=true&w=majority")) as client:
            users = accounts.accounts_count(client.aig, stripe, category)
        return JSONResponse(content=users)

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@app.get('/totalling')
def totalling(request: Request, key: str = "", root: str = "admin@aigia.co.jp", studio: str = ""):
    host, path, _key, username, password = config()
    try:
        return templates.TemplateResponse("totalling.j2",
                                          context={"request": request, "host": host, "path": path, "key": key,
                                                   "rootuser": root, "studio": studio})
    except Exception as e:
        raise HTTPException(status_code=403, detail=e)


@app.get('/api/totalling')
def api_totalling(key: str = "key", studio: str = ""):
    from aig_accounts import accounts, payment
    host, path, _key, username, password = config()
    try:
        stripeconfig = stripe_config()
        stripe = payment.Stripe(stripeconfig['protocol'], stripeconfig['host'], stripeconfig['key'])
        with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                        "aig?retryWrites=true&w=majority")) as client:
            result = accounts.totalling(client.aig, studio, stripe)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=403, detail=e)


@app.get('/guest')
def guest(request: Request, key: str = "", root: str = "admin@aigia.co.jp"):
    host, path, _key, username, password = config()
    return templates.TemplateResponse("guests.j2",
                                      context={"request": request, "host": host, "path": path, "key": key,
                                               "rootuser": root})


@app.get('/api/guest')
def api_guest(key: str = "", root: str = "admin@aigia.co.jp", type: str = "", skip: int = 0, limit: int = 20):
    from aig_accounts import accounts
    host, path, _key, username, password = config()
    _guests = []
    with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                    "aig?retryWrites=true&w=majority")) as client:
        _guests = accounts.guest(client.aig, root, type, skip, limit)
    return JSONResponse(content=_guests)


"""
@app.get('/validation')
def validation(key: str = "key", root: str = "admin@aigia.co.jp"):
    from aig_accounts import accounts
    host, path, _key, username, password = config()
    with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                    "aig?retryWrites=true&w=majority")) as client:
        data = accounts.valid_relation(client.aig, True)
        df = pd.DataFrame(data, columns=["from", "to", "type"])
        output = sister("validation.csv")
        df.to_csv(output, index=False)
    return FileResponse(path=output, media_type='text/csv', filename="validation.csv")

"""
'''
@app.route('/graph', methods=['GET'])
def graph(request: Request, key: str = "key", root: str = "admin@aigia.co.jp", layout: str = 'dot', depth: int = 4):
	from aig_accounts import accounts
	if key is not None:
		host, path, _key, username, password = config()
		if _key == key:
			# circo, dot, fdp, neato, nop, nop1, nop2, osage, patchwork, sfdp, twopi
			with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net" , "aig?retryWrites=true&w=majority")) as client:
				output = sister("aig.svg")
				accounts.relation_graph(client.aig, output, root, depth, layout)
			return FileResponse(path=output, media_type='image/svg+xml', filename="aig.svg")
		else:
			raise HTTPException(status_code=403, detail="invalid key.")
	else:
		raise HTTPException(status_code=403, detail="no key.")
'''


@app.get('/shots')
def shots(request: Request, key: str = "", query: Any = {}, sort: str = "platform.description.score", skip: int = 0,
          limit: int = 20):
    from aig_shots import shots
    host, path, _key, username, password = config()
    columns = [
        "name", "username", "club", "score", "postureScore", "ballisticScore", "studio", "sites",
        "前傾角度.address", "前傾角度.backswing", "前傾角度.top", "前傾角度.halfdown", "前傾角度.impact",
        "前傾角度.follow",
        "前傾角度.finish",
        "背骨の傾き.address", "背骨の傾き.backswing", "背骨の傾き.top", "背骨の傾き.halfdown", "背骨の傾き.impact",
        "背骨の傾き.follow",
        "背骨の傾き.finish",
        "首元の動き.address", "首元の動き.backswing", "首元の動き.top", "首元の動き.halfdown", "首元の動き.impact",
        "首元の動き.follow",
        "首元の動き.finish",
        "右腰の動き.address", "右腰の動き.backswing", "右腰の動き.top", "右腰の動き.halfdown", "右腰の動き.impact",
        "右腰の動き.follow",
        "右腰の動き.finish",
        "左腰の動き.address", "左腰の動き.backswing", "左腰の動き.top", "左腰の動き.halfdown", "左腰の動き.impact",
        "左腰の動き.follow",
        "左腰の動き.finish",
        "重心の動き_正面.address", "重心の動き_正面.backswing", "重心の動き_正面.top", "重心の動き_正面.halfdown",
        "重心の動き_正面.impact",
        "重心の動き_正面.follow", "重心の動き_正面.finish",
        "右膝の角度.address", "右膝の角度.backswing", "右膝の角度.top", "右膝の角度.halfdown", "右膝の角度.impact",
        "右膝の角度.follow",
        "右膝の角度.finish",
        "手元の浮き.address", "手元の浮き.backswing", "手元の浮き.top", "手元の浮き.halfdown", "手元の浮き.impact",
        "手元の浮き.follow",
        "手元の浮き.finish",
        "左膝の角度.address", "左膝の角度.backswing", "左膝の角度.top", "左膝の角度.halfdown", "左膝の角度.impact",
        "左膝の角度.follow",
        "左膝の角度.finish",
        "頭の動き.address", "頭の動き.backswing", "頭の動き.top", "頭の動き.halfdown", "頭の動き.impact", "頭の動き.follow",
        "頭の動き.finish",
        "両肩の傾き_正面.address", "両肩の傾き_正面.backswing", "両肩の傾き_正面.top", "両肩の傾き_正面.halfdown",
        "両肩の傾き_正面.impact",
        "両肩の傾き_正面.follow", "両肩の傾き_正面.finish",
        "重心の動き_後方.address", "重心の動き_後方.backswing", "重心の動き_後方.top", "重心の動き_後方.halfdown",
        "重心の動き_後方.impact",
        "重心の動き_後方.follow", "重心の動き_後方.finish",
        "グリップ位置.address", "グリップ位置.backswing", "グリップ位置.top", "グリップ位置.halfdown", "グリップ位置.impact",
        "グリップ位置.follow",
        "グリップ位置.finish",
        "手首軌道.address", "手首軌道.backswing", "手首軌道.top", "手首軌道.halfdown", "手首軌道.impact",
        "手首軌道.follow",
        "手首軌道.finish",
        "腰の開き.address", "腰の開き.backswing", "腰の開き.top", "腰の開き.halfdown", "腰の開き.impact", "腰の開き.follow",
        "腰の開き.finish",
        "肩の開き.address", "肩の開き.backswing", "肩の開き.top", "肩の開き.halfdown", "肩の開き.impact", "肩の開き.follow",
        "肩の開き.finish",
        "トータル", "トータルブレ", "キャリー", "キャリーブレ", "ヘッドスピード", "ボール初速", "ミート率", "打ち出し角 上下", "打ち出し角 左右",
        "バックスピン",
        "サイドスピン", "ブロー角", "ヘッド軌道", "フェイス角",
    ]

    with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                    "aig?retryWrites=true&w=majority")) as client:
        _shots, columns = shots.shots(client.aig, query, skip, limit, sort, columns)
    return templates.TemplateResponse("shots.j2",
                                      context={"request": request, "host": host, "path": path, "key": key,
                                               "shots": _shots, "columns": columns})


@app.get('/shoting')
def shoting(request: Request, key: str = "", root: str = "admin@aigia.co.jp"):
    host, path, _key, username, password = config()
    return templates.TemplateResponse("shoting.j2",
                                      context={"request": request, "host": host, "path": path, "key": key,
                                               "rootuser": root})


class Item(BaseModel):
    key: str
    count: int = 0


@app.post('/api/shoting')
def shoting(item: Item):
    from aig_accounts import accounts, payment
    host, path, _key, username, password = config()
    try:
        for i in range(item.count):
            print(i, "秒経過2")
            time.sleep(5)
            url = "http://localhost/shotsm?f=/Users/" + os.environ.get(
                "USER") + "/project/aig/data/20200218/20200218-170749.kar"
            r = requests.get(url)
            if i == item.count:
                return JSONResponse(content={})
    except Exception as e:
        raise HTTPException(status_code=403, detail=e)


# raise HTTPException(status_code=403, detail="no key.")


@app.get('/stream/shots')
def stream_shots(key: str = "", query: Any = {}, sort: str = "platform.description.score", skip: int = 0,
                 limit: int = 20):
    from aig_shots import shots
    host, path, _key, username, password = config()
    columns = [
        "name", "username", "club", "score", "postureScore", "ballisticScore", "studio", "sites",
        "前傾角度.address", "前傾角度.backswing", "前傾角度.top", "前傾角度.halfdown", "前傾角度.impact",
        "前傾角度.follow",
        "前傾角度.finish",
        "背骨の傾き.address", "背骨の傾き.backswing", "背骨の傾き.top", "背骨の傾き.halfdown", "背骨の傾き.impact",
        "背骨の傾き.follow",
        "背骨の傾き.finish",
        "首元の動き.address", "首元の動き.backswing", "首元の動き.top", "首元の動き.halfdown", "首元の動き.impact",
        "首元の動き.follow",
        "首元の動き.finish",
        "右腰の動き.address", "右腰の動き.backswing", "右腰の動き.top", "右腰の動き.halfdown", "右腰の動き.impact",
        "右腰の動き.follow",
        "右腰の動き.finish",
        "左腰の動き.address", "左腰の動き.backswing", "左腰の動き.top", "左腰の動き.halfdown", "左腰の動き.impact",
        "左腰の動き.follow",
        "左腰の動き.finish",
        "重心の動き_正面.address", "重心の動き_正面.backswing", "重心の動き_正面.top", "重心の動き_正面.halfdown",
        "重心の動き_正面.impact",
        "重心の動き_正面.follow", "重心の動き_正面.finish",
        "右膝の角度.address", "右膝の角度.backswing", "右膝の角度.top", "右膝の角度.halfdown", "右膝の角度.impact",
        "右膝の角度.follow",
        "右膝の角度.finish",
        "手元の浮き.address", "手元の浮き.backswing", "手元の浮き.top", "手元の浮き.halfdown", "手元の浮き.impact",
        "手元の浮き.follow",
        "手元の浮き.finish",
        "左膝の角度.address", "左膝の角度.backswing", "左膝の角度.top", "左膝の角度.halfdown", "左膝の角度.impact",
        "左膝の角度.follow",
        "左膝の角度.finish",
        "頭の動き.address", "頭の動き.backswing", "頭の動き.top", "頭の動き.halfdown", "頭の動き.impact", "頭の動き.follow",
        "頭の動き.finish",
        "両肩の傾き_正面.address", "両肩の傾き_正面.backswing", "両肩の傾き_正面.top", "両肩の傾き_正面.halfdown",
        "両肩の傾き_正面.impact",
        "両肩の傾き_正面.follow", "両肩の傾き_正面.finish",
        "重心の動き_後方.address", "重心の動き_後方.backswing", "重心の動き_後方.top", "重心の動き_後方.halfdown",
        "重心の動き_後方.impact",
        "重心の動き_後方.follow", "重心の動き_後方.finish",
        "グリップ位置.address", "グリップ位置.backswing", "グリップ位置.top", "グリップ位置.halfdown", "グリップ位置.impact",
        "グリップ位置.follow",
        "グリップ位置.finish",
        "手首軌道.address", "手首軌道.backswing", "手首軌道.top", "手首軌道.halfdown", "手首軌道.impact",
        "手首軌道.follow",
        "手首軌道.finish",
        "腰の開き.address", "腰の開き.backswing", "腰の開き.top", "腰の開き.halfdown", "腰の開き.impact", "腰の開き.follow",
        "腰の開き.finish",
        "肩の開き.address", "肩の開き.backswing", "肩の開き.top", "肩の開き.halfdown", "肩の開き.impact", "肩の開き.follow",
        "肩の開き.finish",
        "トータル", "トータルブレ", "キャリー", "キャリーブレ", "ヘッドスピード", "ボール初速", "ミート率", "打ち出し角 上下", "打ち出し角 左右",
        "バックスピン",
        "サイドスピン", "ブロー角", "ヘッド軌道", "フェイス角",
    ]

    with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                    "aig?retryWrites=true&w=majority")) as client:
        return StreamingResponse(shots.generate_shots(client.aig, query, skip, limit, sort, columns))


@app.get('/download/graph')
def download_graph(key: str = "", root: str = "admin@aigia.co.jp", layout: str = 'dot', depth: int = 4):
    # from aig_accounts import download_accounts
    from aig_accounts import accounts
    host, path, _key, username, password = config()
    # circo, dot, fdp, neato, nop, nop1, nop2, osage, patchwork, sfdp, twopi
    with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                    "aig?retryWrites=true&w=majority")) as client:
        output = sister("aig.svg")
        accounts.relation_graph(client.aig, output, root, depth, layout)
    return FileResponse(path=output, media_type='image/svg+xml', filename="aig.svg")


@app.get('/usernames')
def usernames(key: str = "", type: str = "", skip: int = 0, limit: int = 20):
    from aig_accounts import accounts
    host, path, _key, username, password = config()
    with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                    "aig?retryWrites=true&w=majority")) as client:
        users = accounts.user_by_type(client.aig, type, skip, limit)
    return JSONResponse(content=users)


@app.get('/totallings', response_class=HTMLResponse)
def totallings(request: Request, key: str = ""):
    host, path, _key, username, password = config()
    return templates.TemplateResponse("totallings.j2", context={"request": request, "key": key})

#スタジオでループ

@app.get('/studios')
def studio_list(request: Request):
    host, path, _key, username, password = config()
    with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                    "aig?retryWrites=true&w=majority")) as client:
        studios = []

        accounts = client.aig.accounts

        studio_cursor = accounts.find({"type": "studio"}) #.skip(skip).limit(limit)
        for studio in studio_cursor:
            count_cousor = api_accounts(client, studio["user_id"])
            count = next(count_cousor,None)
            if count is not None:
                studios.append({"name":studio["username"],"nickname":studio["content"]["nickname"], "user_count": count["user_id"]})
        return templates.TemplateResponse("studios.j2", context={"request": request, "studios":studios})

def api_accounts(client,item_id):
    try:

        #target = "636b46c20e2b5ab41da72265"

        pipeline = [
            {'$match': { 'from_id': item_id } },
            {'$graphLookup': {
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
            },
            {'$unwind': {'path': '$belongs'}},
            {'$lookup': {
                    'from': 'accounts',
                    'localField': 'belongs.from_id',
                    'foreignField': 'user_id',
                    'as': 'account'
                }
            },
            {'$unwind': {'path': '$account'}},
            {'$addFields': {'account.depth': '$belongs.depth'}},
            {'$replaceRoot': {'newRoot': '$account'}},
            {'$sort': {'depth': -1}},
            {'$match': {'type': ''}},
            {'$project': {
                    '_id': 0,
                    'publickey': 0,
                    'privatekey': 0,
                    'secret': 0,
                    'salt': 0,
                    'hash': 0
                }
            },
            {'$count': 'user_id'}
        ]

        result = client.aig.relations.aggregate(pipeline)
    #    count = result.next()
        return result #count["user_id"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


# 例外処理
@app.exception_handler(HTTPException)
def api_error_handler(request: Request, exception: HTTPException):
    host, path, key, username, password = config()
    return templates.TemplateResponse("error.j2", context={"request": request, "key": key, "error": exception})


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000, log_level="info")
