import databases
import sqlalchemy

from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.scoping import scoped_session

class MySql:
    def __init__(self):
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
        self.ENGINE = sqlalchemy.create_engine(
            DATABASE_URL, encoding="utf-8", echo=True
        )

        self.database = databases.Database(DATABASE_URL)

        self.sql_metadata = sqlalchemy.MetaData()

        self.sql_metadata.create_all(self.ENGINE)

        # Sessionの作成
        self.session = scoped_session(
            # ORM実行時の設定。自動コミットするか、自動反映するか
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.ENGINE
            )
        )
        # modelで使用する
        self.Base = declarative_base()
        # DB接続用のセッションクラス、インスタンスが作成されると接続する
        self.Base.query = self.session.query_property()

