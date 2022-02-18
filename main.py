#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pm2登録
# pm2 start result.py --name result --interpreter python3

import os
import json
import pathlib

from typing import Any
from datetime import datetime
import time

import uvicorn

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
    # return "mongodb://localhost/aig"
    return protocol + "://" + username + ":" + password + "@" + host + "/" + db


@app.get('/')
def index(request: Request, key: str = "", root: str = "admin@aigia.co.jp", layout: str = "dot"):
    if key is not None:
        host, path, _key, username, password = config()
        if key == _key:
            return templates.TemplateResponse("index.html",
                                              context={"request": request, "host": host, "path": path, "key": _key,
                                                       "rootuser": root, "layout": layout})
        else:
            raise HTTPException(status_code=403, detail="invalid key.")
    else:
        raise HTTPException(status_code=403, detail="no key.")


@app.get('/tree')
def tree(request: Request, key: str = "", root: str = "admin@aigia.co.jp"):
    from aig_accounts import accounts
    if key is not None:
        host, path, _key, username, password = config()
        if _key == key:
            with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                            "aig?retryWrites=true&w=majority")) as client:
                _accounts = accounts.relation_tree(client.aig, root)
            return templates.TemplateResponse("accounts_tree.html",
                                              context={"request": request, "host": host, "path": path, "key": key,
                                                       "rootuser": root, "accounts": _accounts})
        else:
            raise HTTPException(status_code=403, detail="invalid key.")
    else:
        raise HTTPException(status_code=403, detail="no key.")


@app.get('/accounts')
def accounts(request: Request, key: str = "", root: str = "admin@aigia.co.jp"):
    if key is not None:
        host, path, _key, username, password = config()
        if _key == key:
            try:
                return templates.TemplateResponse("accounts.html",
                                                  context={"request": request, "host": host, "path": path, "key": key,
                                                           "rootuser": root})
            except Exception as e:
                raise HTTPException(status_code=500, detail=e)
        else:
            raise HTTPException(status_code=403, detail="invalid key.")
    else:
        raise HTTPException(status_code=403, detail="no key.")


def json_serial(user):
    date = user['date']
    if isinstance(date, (datetime, date)):
        user['date'] = date.isoformat()
    return user


@app.get('/api/accounts')
def api_accounts(key: str = "", skip: int = 0, limit: int = 20, category: str = ""):
    from aig_accounts import accounts, payment
    if key is not None:
        host, path, _key, username, password = config()
        if _key == key:
            try:
                stripeconfig = stripe_config()
                stripe = payment.Stripe(stripeconfig['protocol'], stripeconfig['host'], stripeconfig['key'])
                with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                                "aig?retryWrites=true&w=majority")) as client:
                    users = accounts.accounts(client.aig, skip, limit, stripe, category)
                return JSONResponse(content=list(map(json_serial, users)))
            except Exception as e:
                raise HTTPException(status_code=500, detail=e)
        else:
            raise HTTPException(status_code=403, detail="invalid key.")
    else:
        raise HTTPException(status_code=403, detail="no key.")


@app.get('/api/accounts/count')
def api_accounts(key: str = "", skip: int = 0, category: str = ""):
    from aig_accounts import accounts, payment
    if key is not None:
        host, path, _key, username, password = config()
        if _key == key:
            try:
                stripeconfig = stripe_config()
                stripe = payment.Stripe(stripeconfig['protocol'], stripeconfig['host'], stripeconfig['key'])
                with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                                "aig?retryWrites=true&w=majority")) as client:
                    users = accounts.accounts_count(client.aig, stripe, category)
                return JSONResponse(content=users)

            except Exception as e:
                raise HTTPException(status_code=500, detail=e)
        else:
            raise HTTPException(status_code=403, detail="invalid key.")
    else:
        raise HTTPException(status_code=403, detail="no key.")


@app.get('/totalling')
def totalling(request: Request, key: str = "", root: str = "admin@aigia.co.jp", studio: str = ""):
    if key is not None:
        host, path, _key, username, password = config()
        if _key == key:
            try:
                return templates.TemplateResponse("totalling.html",
                                                  context={"request": request, "host": host, "path": path, "key": key,
                                                           "rootuser": root, "studio": studio})
            except Exception as e:
                raise HTTPException(status_code=403, detail=e)
        else:
            raise HTTPException(status_code=403, detail="invalid key.")
    else:
        raise HTTPException(status_code=403, detail="no key.")


@app.get('/api/totalling')
def api_totalling(key: str = "key", studio: str = ""):
    from aig_accounts import accounts, payment
    if key is not None:
        host, path, _key, username, password = config()
        if _key == key:
            try:
                stripeconfig = stripe_config()
                stripe = payment.Stripe(stripeconfig['protocol'], stripeconfig['host'], stripeconfig['key'])
                with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                                "aig?retryWrites=true&w=majority")) as client:
                    result = accounts.totalling(client.aig, studio, stripe)
                return JSONResponse(content=result)
            except Exception as e:
                raise HTTPException(status_code=403, detail=e)
        else:
            raise HTTPException(status_code=403, detail="invalid key.")
    else:
        raise HTTPException(status_code=403, detail="no key.")


@app.get('/guest')
def guest(request: Request, key: str = "", root: str = "admin@aigia.co.jp"):
    if key is not None:
        host, path, _key, username, password = config()
        if _key == key:
            return templates.TemplateResponse("guests.html",
                                              context={"request": request, "host": host, "path": path, "key": key,
                                                       "rootuser": root})
        else:
            raise HTTPException(status_code=403, detail="invalid key.")
    else:
        raise HTTPException(status_code=403, detail="no key.")


@app.get('/api/guest')
def api_guest(key: str = "", root: str = "admin@aigia.co.jp", type: str = "", skip: int = 0, limit: int = 20):
    from aig_accounts import accounts
    if key is not None:
        host, path, _key, username, password = config()
        if _key == key:
            _guests = []
            with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                            "aig?retryWrites=true&w=majority")) as client:
                _guests = accounts.guest(client.aig, root, type, skip, limit)
            return JSONResponse(content=_guests)
        else:
            raise HTTPException(status_code=403, detail="invalid key.")
    else:
        raise HTTPException(status_code=403, detail="no key.")


@app.get('/validation')
def validation(key: str = "key", root: str = "admin@aigia.co.jp"):
    from aig_accounts import accounts
    if key is not None:
        host, path, _key, username, password = config()
        if _key == key:
            with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                            "aig?retryWrites=true&w=majority")) as client:
                data = accounts.valid_relation(client.aig, True)
                df = pd.DataFrame(data, columns=["from", "to", "type"])
                output = sister("validation.csv")
                df.to_csv(output, index=False)
            return FileResponse(path=output, media_type='text/csv', filename="validation.csv")
        else:
            raise HTTPException(status_code=403, detail="invalid key.")
    else:
        raise HTTPException(status_code=403, detail="no key.")


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
    if key is not None:
        host, path, _key, username, password = config()
        if _key == key:
            columns = [
                "name", "username", "club", "score", "postureScore", "ballisticScore", "studio", "sites",
                "前傾角度.address", "前傾角度.backswing", "前傾角度.top", "前傾角度.halfdown", "前傾角度.impact", "前傾角度.follow",
                "前傾角度.finish",
                "背骨の傾き.address", "背骨の傾き.backswing", "背骨の傾き.top", "背骨の傾き.halfdown", "背骨の傾き.impact", "背骨の傾き.follow",
                "背骨の傾き.finish",
                "首元の動き.address", "首元の動き.backswing", "首元の動き.top", "首元の動き.halfdown", "首元の動き.impact", "首元の動き.follow",
                "首元の動き.finish",
                "右腰の動き.address", "右腰の動き.backswing", "右腰の動き.top", "右腰の動き.halfdown", "右腰の動き.impact", "右腰の動き.follow",
                "右腰の動き.finish",
                "左腰の動き.address", "左腰の動き.backswing", "左腰の動き.top", "左腰の動き.halfdown", "左腰の動き.impact", "左腰の動き.follow",
                "左腰の動き.finish",
                "重心の動き_正面.address", "重心の動き_正面.backswing", "重心の動き_正面.top", "重心の動き_正面.halfdown", "重心の動き_正面.impact",
                "重心の動き_正面.follow", "重心の動き_正面.finish",
                "右膝の角度.address", "右膝の角度.backswing", "右膝の角度.top", "右膝の角度.halfdown", "右膝の角度.impact", "右膝の角度.follow",
                "右膝の角度.finish",
                "手元の浮き.address", "手元の浮き.backswing", "手元の浮き.top", "手元の浮き.halfdown", "手元の浮き.impact", "手元の浮き.follow",
                "手元の浮き.finish",
                "左膝の角度.address", "左膝の角度.backswing", "左膝の角度.top", "左膝の角度.halfdown", "左膝の角度.impact", "左膝の角度.follow",
                "左膝の角度.finish",
                "頭の動き.address", "頭の動き.backswing", "頭の動き.top", "頭の動き.halfdown", "頭の動き.impact", "頭の動き.follow",
                "頭の動き.finish",
                "両肩の傾き_正面.address", "両肩の傾き_正面.backswing", "両肩の傾き_正面.top", "両肩の傾き_正面.halfdown", "両肩の傾き_正面.impact",
                "両肩の傾き_正面.follow", "両肩の傾き_正面.finish",
                "重心の動き_後方.address", "重心の動き_後方.backswing", "重心の動き_後方.top", "重心の動き_後方.halfdown", "重心の動き_後方.impact",
                "重心の動き_後方.follow", "重心の動き_後方.finish",
                "グリップ位置.address", "グリップ位置.backswing", "グリップ位置.top", "グリップ位置.halfdown", "グリップ位置.impact", "グリップ位置.follow",
                "グリップ位置.finish",
                "手首軌道.address", "手首軌道.backswing", "手首軌道.top", "手首軌道.halfdown", "手首軌道.impact", "手首軌道.follow",
                "手首軌道.finish",
                "腰の開き.address", "腰の開き.backswing", "腰の開き.top", "腰の開き.halfdown", "腰の開き.impact", "腰の開き.follow",
                "腰の開き.finish",
                "肩の開き.address", "肩の開き.backswing", "肩の開き.top", "肩の開き.halfdown", "肩の開き.impact", "肩の開き.follow",
                "肩の開き.finish",
                "トータル", "トータルブレ", "キャリー", "キャリーブレ", "ヘッドスピード", "ボール初速", "ミート率", "打ち出し角 上下", "打ち出し角 左右", "バックスピン",
                "サイドスピン", "ブロー角", "ヘッド軌道", "フェイス角",
            ]

            with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                            "aig?retryWrites=true&w=majority")) as client:
                _shots, columns = shots.shots(client.aig, query, skip, limit, sort, columns)
            return templates.TemplateResponse("shots.html",
                                              context={"request": request, "host": host, "path": path, "key": key,
                                                       "shots": _shots, "columns": columns})
        else:
            raise HTTPException(status_code=403, detail="invalid key.")
    else:
        raise HTTPException(status_code=403, detail="no key.")


@app.get('/shoting')
def shoting(request: Request, key: str = "", root: str = "admin@aigia.co.jp"):
    if key is not None:
        host, path, _key, username, password = config()
        if _key == key:
            return templates.TemplateResponse("shoting.html",
                                              context={"request": request, "host": host, "path": path, "key": key,
                                                       "rootuser": root})
        else:
            raise HTTPException(status_code=403, detail="invalid key.")
    else:
        raise HTTPException(status_code=403, detail="no key.")

class Item(BaseModel):
    key: str
    count: int = 0

@app.post('/api/shoting')
def shoting(item: Item):
    from aig_accounts import accounts, payment
    if item.key is not None:
        host, path, _key, username, password = config()
        if _key == item.key:
            try:
                for i in range(item.count):
                    print(i, "秒経過2")
                    time.sleep(5)
                    url = "http://localhost/shotsm?f=/Users/" + os.environ.get("USER") + "/project/aig/data/20200218/20200218-170749.kar";
                    r = requests.get(url)
                    if i == item.count:
                        return JSONResponse(content={})
            except Exception as e:
                raise HTTPException(status_code=403, detail=e)
        else:
            raise HTTPException(status_code=403, detail="invalid key.")
    else:
        raise HTTPException(status_code=403, detail="no key.")


# raise HTTPException(status_code=403, detail="no key.")


@app.get('/stream/shots')
def stream_shots(key: str = "", query: Any = {}, sort: str = "platform.description.score", skip: int = 0,
                 limit: int = 20):
    from aig_shots import shots
    if key is not None:
        host, path, _key, username, password = config()
        if _key == key:
            columns = [
                "name", "username", "club", "score", "postureScore", "ballisticScore", "studio", "sites",
                "前傾角度.address", "前傾角度.backswing", "前傾角度.top", "前傾角度.halfdown", "前傾角度.impact", "前傾角度.follow",
                "前傾角度.finish",
                "背骨の傾き.address", "背骨の傾き.backswing", "背骨の傾き.top", "背骨の傾き.halfdown", "背骨の傾き.impact", "背骨の傾き.follow",
                "背骨の傾き.finish",
                "首元の動き.address", "首元の動き.backswing", "首元の動き.top", "首元の動き.halfdown", "首元の動き.impact", "首元の動き.follow",
                "首元の動き.finish",
                "右腰の動き.address", "右腰の動き.backswing", "右腰の動き.top", "右腰の動き.halfdown", "右腰の動き.impact", "右腰の動き.follow",
                "右腰の動き.finish",
                "左腰の動き.address", "左腰の動き.backswing", "左腰の動き.top", "左腰の動き.halfdown", "左腰の動き.impact", "左腰の動き.follow",
                "左腰の動き.finish",
                "重心の動き_正面.address", "重心の動き_正面.backswing", "重心の動き_正面.top", "重心の動き_正面.halfdown", "重心の動き_正面.impact",
                "重心の動き_正面.follow", "重心の動き_正面.finish",
                "右膝の角度.address", "右膝の角度.backswing", "右膝の角度.top", "右膝の角度.halfdown", "右膝の角度.impact", "右膝の角度.follow",
                "右膝の角度.finish",
                "手元の浮き.address", "手元の浮き.backswing", "手元の浮き.top", "手元の浮き.halfdown", "手元の浮き.impact", "手元の浮き.follow",
                "手元の浮き.finish",
                "左膝の角度.address", "左膝の角度.backswing", "左膝の角度.top", "左膝の角度.halfdown", "左膝の角度.impact", "左膝の角度.follow",
                "左膝の角度.finish",
                "頭の動き.address", "頭の動き.backswing", "頭の動き.top", "頭の動き.halfdown", "頭の動き.impact", "頭の動き.follow",
                "頭の動き.finish",
                "両肩の傾き_正面.address", "両肩の傾き_正面.backswing", "両肩の傾き_正面.top", "両肩の傾き_正面.halfdown", "両肩の傾き_正面.impact",
                "両肩の傾き_正面.follow", "両肩の傾き_正面.finish",
                "重心の動き_後方.address", "重心の動き_後方.backswing", "重心の動き_後方.top", "重心の動き_後方.halfdown", "重心の動き_後方.impact",
                "重心の動き_後方.follow", "重心の動き_後方.finish",
                "グリップ位置.address", "グリップ位置.backswing", "グリップ位置.top", "グリップ位置.halfdown", "グリップ位置.impact", "グリップ位置.follow",
                "グリップ位置.finish",
                "手首軌道.address", "手首軌道.backswing", "手首軌道.top", "手首軌道.halfdown", "手首軌道.impact", "手首軌道.follow",
                "手首軌道.finish",
                "腰の開き.address", "腰の開き.backswing", "腰の開き.top", "腰の開き.halfdown", "腰の開き.impact", "腰の開き.follow",
                "腰の開き.finish",
                "肩の開き.address", "肩の開き.backswing", "肩の開き.top", "肩の開き.halfdown", "肩の開き.impact", "肩の開き.follow",
                "肩の開き.finish",
                "トータル", "トータルブレ", "キャリー", "キャリーブレ", "ヘッドスピード", "ボール初速", "ミート率", "打ち出し角 上下", "打ち出し角 左右", "バックスピン",
                "サイドスピン", "ブロー角", "ヘッド軌道", "フェイス角",
            ]

            with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                            "aig?retryWrites=true&w=majority")) as client:
                return StreamingResponse(shots.generate_shots(client.aig, query, skip, limit, sort, columns))
        else:
            raise HTTPException(status_code=403, detail="invalid key.")
    else:
        raise HTTPException(status_code=403, detail="no key.")


@app.get('/download/tree')
def download_tree(key: str = "", root: str = "admin@aigia.co.jp"):
    from aig_accounts import download_accounts
    if key is not None:
        host, path, _key, username, password = config()
        if _key == key:
            with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                            "aig?retryWrites=true&w=majority")) as client:
                columns = ["depth", "username"]
                data = download_accounts.relation_tree(client.aig, root)
                df = pd.DataFrame(data, columns=columns)
                output = sister("tree.csv")
                df.to_csv(output, index=False)
            return FileResponse(path=output, media_type='text/csv', filename="tree.csv")
        else:
            raise HTTPException(status_code=403, detail="invalid key.")
    else:
        raise HTTPException(status_code=403, detail="no key.")


@app.get('/download/accounts')
def download_accounts(key: str = ""):
    from aig_accounts import download_accounts, payment
    if key is not None:
        host, path, _key, username, password = config()
        if _key == key:
            stripeconfig = stripe_config()
            stripe = payment.Stripe(stripeconfig['protocol'], stripeconfig['host'], stripeconfig['key'])
            with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                            "aig?retryWrites=true&w=majority")) as client:
                columns = ["company", "studio", "user", "username", "type", "subscribe", "date"]
                data = download_accounts.accounts(client.aig, stripe)
                df = pd.DataFrame(data, columns=columns)
                output = sister("accounts.xlsx")
                df.to_excel(output, sheet_name="account", header=True)
            return FileResponse(path=output,
                                media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                filename="accounts.xlsx")
        else:
            raise HTTPException(status_code=403, detail="invalid key.")
    else:
        raise HTTPException(status_code=403, detail="no key.")


@app.get('/download/guest')
def download_guest(key: str = "", root: str = "admin@aigia.co.jp", type: str = ""):
    from aig_accounts import download_accounts
    if key is not None:
        host, path, _key, username, password = config()
        if _key == key:
            with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                            "aig?retryWrites=true&w=majority")) as client:
                columns = ["username", "type", 'stripe_id']
                data = download_accounts.guest(client.aig, root, type)
                df = pd.DataFrame(data, columns=columns)
                output = sister("guests.csv")
                df.to_csv(output, index=False)
            return FileResponse(path=output, media_type='text/csv', filename="guests.csv")
        else:
            raise HTTPException(status_code=403, detail="invalid key.")
    else:
        raise HTTPException(status_code=403, detail="no key.")


@app.get('/download/validation')
def download_validation(key: str = ""):
    from aig_accounts import download_accounts
    if key is not None:
        host, path, _key, username, password = config()
        if _key == key:
            with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                            "aig?retryWrites=true&w=majority")) as client:
                columns = ["from", "to", "type"]
                data = download_accounts.valid_relation(client.aig, True)
                df = pd.DataFrame(data, columns=columns)
                output = sister("validation.csv")
                df.to_csv(output, index=False)
            return FileResponse(path=output, media_type='text/csv', filename="validation.csv")
        else:
            raise HTTPException(status_code=403, detail="invalid key.")
    else:
        raise HTTPException(status_code=403, detail="no key.")


@app.get('/download/graph')
def download_graph(key: str = "", root: str = "admin@aigia.co.jp", layout: str = 'dot', depth: int = 4):
    from aig_accounts import download_accounts
    if key is not None:
        host, path, _key, username, password = config()
        if _key == key:
            # circo, dot, fdp, neato, nop, nop1, nop2, osage, patchwork, sfdp, twopi
            with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                            "aig?retryWrites=true&w=majority")) as client:
                output = sister("aig.svg")
                download_accounts.relation_graph(client.aig, output, root, depth, layout)
            return FileResponse(path=output, media_type='image/svg+xml', filename="aig.svg")
        else:
            raise HTTPException(status_code=403, detail="invalid key.")
    else:
        raise HTTPException(status_code=403, detail="no key.")


@app.get('/download/shots')
def download_shots(key: str = ""):
    from aig_shots import download_shots
    if key is not None:
        host, path, _key, username, password = config()
        if _key == key:
            with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                            "aig?retryWrites=true&w=majority")) as client:
                columns = ['name', 'username', 'club', 'score', 'postureScore', 'ballisticScore', 'studio', 'sites',
                           "前傾角度.address", "前傾角度.backswing"]
                data = download_shots.shots(client.aig, columns)
                df = pd.DataFrame(data, columns=columns)
                output = sister("shots.csv")
                df.to_csv(output, index=False)
            return FileResponse(path=output, media_type='text/csv', filename="shots.csv")
        else:
            raise HTTPException(status_code=403, detail="no key.")
    else:
        raise HTTPException(status_code=403, detail="no key.")


@app.get('/usernames')
def usernames(key: str = "", type: str = "", skip: int = 0, limit: int = 20):
    from aig_accounts import accounts
    if key is not None:
        host, path, _key, username, password = config()
        if _key == key:
            with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                            "aig?retryWrites=true&w=majority")) as client:
                users = accounts.user_by_type(client.aig, type, skip, limit)
            return JSONResponse(content=users)


@app.get('/totallings', response_class=HTMLResponse)
def totallings(request: Request, key: str = ""):
    if key is not None:
        host, path, _key, username, password = config()
        if _key == key:
            return templates.TemplateResponse("totallings.html", context={"request": request, "key": key})


@app.exception_handler(HTTPException)
def api_error_handler(request: Request, exception: HTTPException):
    host, path, key, username, password = config()
    return templates.TemplateResponse("error.html", context={"request": request, "key": key, "error": exception})


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000, log_level="info")
