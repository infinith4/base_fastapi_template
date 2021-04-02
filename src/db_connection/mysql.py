import databases
import sqlalchemy

from models.user import UserTable, User  # 今回使うモデルをインポート
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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

database = databases.Database(DATABASE_URL)

sql_metadata = sqlalchemy.MetaData()


sql_metadata.create_all(ENGINE)
