from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel

import databases
import sqlalchemy
# 接続したいDBの基本情報を設定
user_name = "docker" #"root"
password = "docker" # "root"
host = "127.0.0.1"  # docker-composeで定義したMySQLのサービス名
database_name = "test_database"

DATABASE_URL = 'mysql://%s:%s@%s/%s?charset=utf8' % (
    user_name,
    password,
    host,
    database_name,
)

# DBとの接続
engine = sqlalchemy.create_engine(
    DATABASE_URL, encoding="utf-8", echo=True
)

database = databases.Database(DATABASE_URL)

sql_metadata = sqlalchemy.MetaData()

app = FastAPI(
    title='FastAPIでつくるtoDoアプリケーション',
    description='FastAPIチュートリアル：FastAPI(とstarlette)でシンプルなtoDoアプリを作りましょう．',
    version='0.9 beta'
)

sql_metadata.create_all(engine)


class NoteIn(BaseModel):
    text: str
    completed: bool


class Note(BaseModel):
    id: int
    text: str
    completed: bool

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# 各タグの説明
tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(
    title="FastAPI Sample Project",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="1.0.1",
    openapi_tags=tags_metadata,
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
    )

templates = Jinja2Templates(directory="src/templates")

app.mount("/static", StaticFiles(directory="src/static"), name="static")

@app.get(
    "/index",
    tags=["root"],
    response_class=HTMLResponse
    )
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "id": 1})

@app.get(
    "/admin",
    tags=["admin"],
    response_class=HTMLResponse
    )
async def admin(request: Request):
    return templates.TemplateResponse('admin.html',
                                      {'request': request,
                                       'username': 'admin'})