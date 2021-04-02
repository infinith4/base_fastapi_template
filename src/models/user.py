# モデルの定義
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel

import sqlalchemy
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm.scoping import scoped_session


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
ENGINE = sqlalchemy.create_engine(
    DATABASE_URL, encoding="utf-8", echo=True
)


# Sessionの作成
session = scoped_session(
    # ORM実行時の設定。自動コミットするか、自動反映するか
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE
    )
)
# modelで使用する
Base = declarative_base()
# DB接続用のセッションクラス、インスタンスが作成されると接続する
Base.query = session.query_property()


# userテーブルのモデルUserTableを定義
class UserTable(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    age = Column(Integer)


# POSTやPUTのとき受け取るRequest Bodyのモデルを定義
class User(BaseModel):
    id: int
    name: str
    age: int


# def main():
#     # テーブルが存在しなければ、テーブルを作成
#     Base.metadata.create_all(bind=ENGINE)


# if __name__ == "__main__":
#     main()