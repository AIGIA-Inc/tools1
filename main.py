#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pm2登録
# pm2 start main.py --name reporter --interpreter python3

import os
import json
import pathlib
import pandas as pd
import uvicorn
import shutil


from datetime import datetime
from pymongo import MongoClient
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pathlib import Path
from tempfile import NamedTemporaryFile
from fastapi import Depends, File, HTTPException, UploadFile, status

#logging.basicConfig(format='%(levelname)s:%(asctime)s:%(pathname)s:%(lineno)s:%(message)s')
#logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)

app = FastAPI()

PATH_ROOT = str(pathlib.Path(__file__).resolve().parent)
PATH_TEMPLATES = str(pathlib.Path(__file__).resolve().parent / "templates")
PATH_STATIC = str(pathlib.Path(__file__).resolve().parent / "static")
PATH_UPLOAD = str(pathlib.Path(__file__).resolve().parent / "data") + "/upload.csv"

app.mount("/static", StaticFiles(directory=PATH_STATIC), name="static")
templates = Jinja2Templates(directory=PATH_TEMPLATES)

def debug(message):
    logger.debug(message, stacklevel=2)

def info(message):
    logger.info(message, stacklevel=2)

def error(message):
    logger.error(message, stacklevel=2)

class User(BaseModel):
    username: str
    password: str

class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    # Configure application to store and get JWT from cookies
    authjwt_token_location: set = {"cookies"}
    # Disable CSRF Protection for this example. default is True
    authjwt_cookie_csrf_protect: bool = False

@AuthJWT.load_config
def get_config():
    return Settings()

# 例外処理
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return templates.TemplateResponse("error.j2", context={"request": request, "error": exc})


@app.post('/login')
def login(user: User, Authorize: AuthJWT = Depends()):
    try:
        if user.username == "aigia" and user.password == "1terabyte":
            # Create the tokens and passing to set_access_cookies or set_refresh_cookies
            access_token = Authorize.create_access_token(subject=user.username)
            refresh_token = Authorize.create_refresh_token(subject=user.username)

            # Set the JWT cookies in the response
            Authorize.set_access_cookies(access_token)
            Authorize.set_refresh_cookies(refresh_token)

            #return templates.TemplateResponse("logged_in.j2", context={"request": request})
            result = {"code": 0,"message": "login success."}
        else:
            result  ={"code": -1,"message": "user not found or invalid password "}
        return result
    except Exception as e:
        raise HTTPException(status_code=403, detail=e)

@app.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    # Set the JWT cookies in the response
    Authorize.set_access_cookies(new_access_token)
    return {"msg":"The token has been refresh"}

@app.post('/logout')
def logout(Authorize: AuthJWT = Depends()):
    """
    Because the JWT are stored in an httponly cookie now, we cannot
    log the user out by simply deleting the cookies in the frontend.
    We need the backend to send us a response to delete the cookies.
    """
    Authorize.jwt_required()
    Authorize.unset_jwt_cookies()
    result = {"code": 0,"message": "logout success."}
    return result
    # return templates.TemplateResponse("base.j2", context={"request": request})


@app.get('/protected')
def protected(Authorize: AuthJWT = Depends()):
    """
    We do not need to make any changes to our protected endpoints. They
    will all still function the exact same as they do when sending the
    JWT in via a headers instead of a cookies
    """
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}


KB = 1024
MB = 1024 * KB

@app.post("/upload")
def upload_file(upload_file: UploadFile = File(...)):
    # ファイルサイズ検証
    upload_file.file.seek(0, 2)  # シークしてサイズ検証
    file_size = upload_file.file.tell()
    if file_size > 20 * MB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="アップロードファイルは20MB制限です",
        )
    else:
        upload_file.file.seek(0)  # シークを戻す

    tmp_path: Path = ""
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
            print(tmp_path)
    except Exception as e:
        print(f"一時ファイル作成: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="一時ファイル作成できません",
        )
    finally:
        upload_file.file.close()

    shutil.move(tmp_path, PATH_UPLOAD)
    result = {"code": 0,"message": "logout success."}

    return result


def sister(name):
    return os.path.expanduser(os.path.join(PATH_ROOT, name))


def config():
    json_open = open('config/default.json', 'r')
    json_load = json.load(json_open)

    host = json_load['host']
    path = json_load['path']
    username = json_load['username']
    password = json_load['password']
    return host, path, username, password


def stripe_config():
    json_open = open('config/default.json', 'r')
    json_load = json.load(json_open)
    stripe = json_load['stripe']
    return stripe


def connect_string(protocol, username, password, host, db):
    #ローカル接続
    #return "mongodb://localhost/aig"
    #待機系接続
    return protocol + "://" + username + ":" + password + "@" + host + "/" + db

def stripe_data(filepath):
    customer_email = []
    try:
        df = pd.read_csv(filepath)
        stripe_df = pd.DataFrame(data=df)
        customer_email = stripe_df.loc[:, "Customer Email"].to_list()
    except Exception as e:
        error("stripe_data")
    finally:
        return customer_email


@app.get('/test')
def studio_list(request: Request):
    return templates.TemplateResponse("test.j2", context={"request": request})


@app.get('/draw')
def index(request: Request, root: str = "admin@aigia.co.jp", layout: str = "fdp",Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    host, path, username, password = config()
    return templates.TemplateResponse("index.j2",  context={"request": request, "host": host, "path": path, "rootuser": root, "layout": layout})


@app.get('/accounts')
def accounts(request: Request, root: str = "admin@aigia.co.jp"):
    host, path, username, password = config()

    try:
        return templates.TemplateResponse("accounts.j2",
                                          context={"request": request, "host": host, "path": path,
                                                   "rootuser": root})
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


def json_serial(user):
    date = user['date']
    if isinstance(date, (datetime, date)):
        user['date'] = date.isoformat()
    return user


@app.get('/api/accounts')
def api_accounts(skip: int = 0, limit: int = 20, category: str = ""):
    from aig_accounts import accounts, payment

    host, path, username, password = config()

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
def api_accounts(skip: int = 0, category: str = ""):
    from aig_accounts import accounts, payment
    host, path, username, password = config()

    try:
        stripeconfig = stripe_config()
        stripe = payment.Stripe(stripeconfig['protocol'], stripeconfig['host'], stripeconfig['key'])
        with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                        "aig?retryWrites=true&w=majority")) as client:
            users = accounts.accounts_count(client.aig, stripe, category)
        return JSONResponse(content=users)

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)





class Item(BaseModel):
    key: str
    count: int = 0

@app.get('/download/graph')
def download_graph(root: str = "admin@aigia.co.jp", layout: str = 'dot', depth: int = 4):
    # from aig_accounts import download_accounts
    from aig_accounts import accounts
    host, path, username, password = config()
    # circo, dot, fdp, neato, nop, nop1, nop2, osage, patchwork, sfdp, twopi
    with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                    "aig?retryWrites=true&w=majority")) as client:
        output = sister("aig.svg")
        accounts.relation_graph(client.aig, output, root, depth, layout)
    return FileResponse(path=output, media_type='image/svg+xml', filename="aig.svg")


@app.get('/usernames')
def usernames(type: str = "", skip: int = 0, limit: int = 20):
    from aig_accounts import accounts
    host, path, username, password = config()
    with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net",
                                    "aig?retryWrites=true&w=majority")) as client:
        users = accounts.user_by_type(client.aig, type, skip, limit)
    return JSONResponse(content=users)

@app.get('/totallings', response_class=HTMLResponse)
def totallings(request: Request):
    host, path, username, password = config()
    return templates.TemplateResponse("totallings.j2", context={"request": request})



@app.get('/')
def auth(request: Request):
    return templates.TemplateResponse("auth.j2", context={"request": request})

@app.get('/main')
def studio_list(request: Request, Authorize: AuthJWT = Depends()):

    return templates.TemplateResponse("studios.j2", context={"request": request})

@app.get('/api/studios/{sort_field}/{sort_order_param}')
# def studio_list(request: Request, Authorize: AuthJWT = Depends()):
def studio_list(sort_field, sort_order_param, Authorize: AuthJWT = Depends()):

    sort_order = sort_order_param == "True"

    df = pd.read_csv("data/upload.csv")
    stripe_df = pd.DataFrame(data=df)
    customer_email = stripe_df.loc[:, "Customer Email"].to_list()

    studios = []
    Authorize.jwt_required()
    host, path, username, password = config()
    with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net", "aig?retryWrites=true&w=majority")) as client:
        accounts = client.aig.accounts
        studio_cursor = accounts.find({"type": "studio"}, sort=[('username',1)]) #.skip(skip).limit(limit)
        for studio in studio_cursor:
            valid_count = 0
            all_count = 0
            user_cousor = studio_users(client, studio["user_id"])
            try:
                while True:
                    user = next(user_cousor,None)
                    if user is not None:
                        all_count += 1
                        for username in customer_email:
                            if user["username"] == username:
                                valid_count+=1
                    else:
                        break
            except Exception as e:
                print(e)
            studios.append({"name":studio["username"],"nickname":studio["content"]["nickname"], "valid_count":valid_count, "all_count": all_count})

    studios = sorted(studios, key=lambda item: item[sort_field], reverse=sort_order)

    total_valid = sum([i['valid_count'] for i in studios])
    total_all = sum([i['all_count'] for i in studios])
    studios.append({"name": "合計", "nickname": "", "valid_count": total_valid, "all_count": total_all})

    return JSONResponse(content=studios)

def api_accounts(client_studio,item_id):
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

        result = client_studio.aig.relations.aggregate(pipeline)
    #    count = result.next()
        return result #count["user_id"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

def studio_users(client,item_id):
    try:
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
            {'$project': {
                    '_id': 0,
                    'publickey': 0,
                    'privatekey': 0,
                    'secret': 0,
                    'salt': 0,
                    'hash': 0
                }
            },
            {'$unwind': {'path': '$username'}}
        ]
        result = client.aig.relations.aggregate(pipeline)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

#stripeのcsvをDataframeに変換




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")


