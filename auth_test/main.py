import uvicorn
import pathlib
import logging
import json
import pandas as pd

from fastapi import Depends, FastAPI,Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from auth import get_current_user, get_current_user_with_refresh_token, create_tokens, authenticate
from pymongo import MongoClient
from fastapi.responses import JSONResponse
from fastapi import Depends, File, HTTPException, UploadFile, status

logging.basicConfig(format='%(levelname)s:%(asctime)s:%(pathname)s:%(lineno)s:%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = FastAPI()

PATH_TEMPLATES = str(pathlib.Path(__file__).resolve().parent.parent / "templates")
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
    json_open = open('../config/default.json', 'r')
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


@app.post("/token", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    """トークン発行"""
    user = authenticate(form.username, form.password)
    return create_tokens(user.id)

@app.get("/refresh_token/", response_model=Token)
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


@app.get('/api/studios/{sort_field}/{sort_order_param}')
def studio_list(sort_field, sort_order_param):

    sort_order = sort_order_param == "True"

    code = -2
    studios = []
    message= ""
    try:
        host, path, username, password = config()
        usernames = stripe_data("../data/upload.csv")
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
        studios.append({"name": "合計", "nickname": "", "valid_count": total_valid, "all_count": total_all})

        return JSONResponse(content={"studios":studios,"code":code, "message":message})
    except Exception as e:
        error(e.message)



#@app.get("/hoge", response_model=User)
#async def read_users_me(current_user: User = Depends(get_current_user)):
#    """ログイン中のユーザーを取得"""
#    print(current_user)
#    return current_user
"""
@app.get('/api/studios', response_model=User)
def studio_list(current_user: User = Depends(get_current_user)):
    #print(current_user)
    code = -2
    studios = []
    message= ""
    try:
        host, path, username, password = config()
        usernames = stripe_data("../data/upload.csv")
        with MongoClient(connect_string("mongodb+srv", username, password, "cluster0.od1kc.mongodb.net", "aig?retryWrites=true&w=majority")) as client:
            if client:
                aig = client.aig
                if aig:
                    accounts = client.aig.accounts
                    studio_cursor = accounts.find({"type": "studio"}) #.skip(skip).limit(limit)
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
                                        message= "dataフォルダーにupload.csvが入っていません."
                                else:
                                    break
                        except Exception as e:
                            error(e.message)

                        studios.append({"name":studio["username"],"nickname":studio["content"]["nickname"], "valid_count":valid_count, "all_count": all_count})
                    total_valid = sum([i['valid_count'] for i in studios])
                    total_all = sum([i['all_count'] for i in studios])
                    studios.append({"name": "合計", "nickname": "", "valid_count": total_valid,"all_count": total_all})

        return JSONResponse(content={"studios":studios,"code":code, "message":message})
    except Exception as e:
        error(e.message)
"""






if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")