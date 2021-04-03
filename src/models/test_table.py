# モデルの定義
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
import db_connection

# userテーブルのモデルUserTableを定義
class TestTable(db_connection.my_sql.Base):
    __tablename__ = 'test_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)

# POSTやPUTのとき受け取るRequest Bodyのモデルを定義
class Test(BaseModel):
    id: int
    name: str

def main():
    # テーブルが存在しなければ、テーブルを作成
    db_connection.my_sql.Base.metadata.create_all(bind=db_connection.my_sql.ENGINE)

if __name__ == "__main__":
    main()