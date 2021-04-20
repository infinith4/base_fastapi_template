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
    "/admin",
    tags=["admin"],
    response_class=HTMLResponse
    )
async def admin(request: Request):
    return templates.TemplateResponse('admin.html',
                                      {'request': request,
                                       'username': 'admin'})