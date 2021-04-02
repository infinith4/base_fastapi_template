# モデルの定義
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from db_connection.mysql import MySql

mySql = MySql()
# userテーブルのモデルUserTableを定義
class UserTable(mySql.Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    age = Column(Integer)

# POSTやPUTのとき受け取るRequest Bodyのモデルを定義
class User(BaseModel):
    id: int
    name: str
    age: int


def main():
    mySql = MySql()
    # テーブルが存在しなければ、テーブルを作成
    mySql.Base.metadata.create_all(bind=mySql.ENGINE)


if __name__ == "__main__":
    main()