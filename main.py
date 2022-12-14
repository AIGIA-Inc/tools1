import uvicorn
import pathlib
import logging
import json
import pandas as pd
import os
import shutil

from fastapi import FastAPI,Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from auth import get_current_user, get_current_user_with_refresh_token, create_tokens, authenticate
from pymongo import MongoClient
from fastapi.responses import JSONResponse
from fastapi import Depends, File, HTTPException, UploadFile, status
from fastapi.staticfiles import StaticFiles
from tempfile import NamedTemporaryFile
from pathlib import Path
from fastapi.responses import FileResponse

app = FastAPI()

logging.basicConfig(format='%(levelname)s:%(asctime)s:%(pathname)s:%(lineno)s:%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

PATH_ROOT = str(pathlib.Path(__file__).resolve().parent)

#デプロイ時　parent.parent→　parent　要修正

PATH_TEMPLATES = str(pathlib.Path(__file__).resolve().parent / "templates")
PATH_UPLOAD = str(pathlib.Path(__file__).resolve().parent / "data") + "/upload.csv"

app.mount("/data", StaticFiles(directory="data"), name="data")
templates = Jinja2Templates(directory=PATH_TEMPLATES)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        orm_mode = True

class User(BaseModel):
    name: str

    class Config:
        orm_mode = True

def error(message):
    logger.error(message, stacklevel=2)

def connect_string(protocol, username, password, host, db):
    #ローカル接続
    #return "mongodb://localhost/aig"
    #待機系接続
    return protocol + "://" + username + ":" + password + "@" + host + "/" + db

def config():
    json_open = open('config/default.json', 'r')
    json_load = json.load(json_open)

    host = json_load['host']
    path = json_load['path']
    username = json_load['username']
    password = json_load['password']
    return host, path, username, password

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


def sister(name):
    return os.path.expanduser(os.path.join(PATH_ROOT, name))

@app.post("/token", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    """トークン発行"""
    user = authenticate(form.username, form.password)
    return create_tokens(user.id)

@app.get("/refresh", response_model=Token)
async def refresh_token(current_user: User = Depends(get_current_user_with_refresh_token)):
    """リフレッシュトークンでトークンを再取得"""
    return create_tokens(current_user.id)

@app.get('/')
def auth(request: Request):
    try:
        return templates.TemplateResponse("base.j2", context={"request": request})
    except Exception as e:
        print(e)
        error("auth")

@app.get('/file_exist')
def file_exist():
    path = 'data/upload.csv'
    is_file = os.path.isfile(path)
    if is_file:
        code = 1
        return JSONResponse(content={"code":code})
    else:
        pass # パスが存在しないかファイルではない

@app.get('/api/studios/{sort_field}/{sort_order_param}', response_model=User)
async def read_users_me(sort_field, sort_order_param, current_user: User = Depends(get_current_user)):
    sort_order = sort_order_param == "True"

#    user = current_user
    code = -2
    studios = []
    message= ""
    try:
        host, path, username, password = config()
        usernames = stripe_data("data/upload.csv")
        with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net", "aig?retryWrites=true&w=majority")) as client:
            if client:
                aig = client.aig
                if aig:
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
                                    if len(usernames) > 0:
                                        for username in usernames:
                                            if user["username"] == username:
                                                valid_count+=1
                                    else:
                                        code = -1
                                        message = "dataフォルダーにupload.csvが入っていません."
                                else:
                                    break
                        except Exception as e:
                            error(e.message)

                        studios.append({"name":studio["username"],"nickname":studio["content"]["nickname"], "valid_count":valid_count, "all_count": all_count})

        studios = sorted(studios, key=lambda item: item[sort_field], reverse=sort_order)

        total_valid = sum([i['valid_count'] for i in studios])
        total_all = sum([i['all_count'] for i in studios])
        studios.append({"name": "admin@aigia.co.jp", "nickname": "合計", "valid_count": total_valid, "all_count": total_all})

        return JSONResponse(content={"studios":studios,"code":code, "message":message})
    except Exception as e:
        error(e.message)



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

@app.get('/draw')
def index(request: Request, root: str = "egai-ikebukuro@earth-academy.co.jp", layout: str = "fdp"):
    host, path, username, password = config()
    return templates.TemplateResponse("index.j2", context={"request": request, "host": host, "path": path, "rootuser": root, "layout": layout})

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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")