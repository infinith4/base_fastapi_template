from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware  # CORSを回避するために必要

import db_connection

from models.user import UserTable, User  # 今回使うモデルをインポート
from models.test_table import TestTable, Test  # 今回使うモデルをインポート

from controllers._base_controller import app, templates

@app.get(
    "/users",
    tags=["user"],
    response_class=HTMLResponse)
def users(request: Request):
    users = db_connection.my_sql.session.query(UserTable).all()
    return templates.TemplateResponse('user_list.html',
                                      {'request': request,
                                       'users': users})

@app.post(
    "/user/{user_id}",
    tags=["user"],
    response_class=HTMLResponse)
def user(user_id: str, request: Request):
    user_data = UserTable()
    user_data.name = f'太郎{user_id}'
    db_connection.my_sql.session.add(user_data)
    db_connection.my_sql.session.commit()

    users = db_connection.my_sql.session.query(UserTable).all()
    return templates.TemplateResponse('user_list.html',
                                      {'request': request,
                                       'users': users})