from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware  # CORSを回避するために必要

from db_connection.mysql import session, database  # DBと接続するためのセッション
from models.user import UserTable, User  # 今回使うモデルをインポート

app = FastAPI(
    title='FastAPIでつくるtoDoアプリケーション',
    description='FastAPIチュートリアル：FastAPI(とstarlette)でシンプルなtoDoアプリを作りましょう．',
    version='0.9 beta'
)

# CORSを回避するために設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# ----------APIの実装------------
# テーブルにいる全ユーザ情報を取得 GET
@app.get("/users")
def read_users():
    users = session.query(UserTable).all()
    return users

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