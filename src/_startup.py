from fastapi import FastAPI, Query, Path, Body
from typing import Optional
from pydantic import BaseModel, Field

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

items = {
    1: {"item_no": 1, "item_name": "name1", "price": 100},
    2: {"item_no": 2, "item_name": "name2", "price": 200},
    3: {"item_no": 3, "item_name": "name3", "price": 300},
}

users = {
    1: {"user_no": 1, "user_name": "name1", "email": "name1@example.com"},
    2: {"user_no": 2, "user_name": "name2", "email": "name2@example.com"},
    3: {"user_no": 3, "user_name": "name3", "email": "name3@example.com"},
}

# スキーマの説明、データ例
class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        None,
        title="The description of the item",
        max_length=300
    )
    price: float = Field(
        ...,
        gt=0,
        description="The price must be greater than zero"
    )
    tax: Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "example_name",
                "description": "example_description",
                "price": 100,
                "tax": 10,
            }
        }

# OpenAPI自体の設定
app = FastAPI(
    title="FastAPI Sample Project",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="1.0.1",
    openapi_tags=tags_metadata,
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
)

# 各urlの設定
@app.get(
    "/items",
    tags=["items"],
    summary="read items summary",
)
async def read_items(
    option: Optional[str] = Query(
        None,
        title="Query Parameter Title",
        description="Query Parameter Description",
    ),
):
    return {"items": items}

@app.get(
    "/items/{item_no}",
    tags=["items"],
    summary="read item summary",
)
async def read_item(
    item_no: str = Path(
        None,
        title="Path Parameter Title",
        description="Path Parameter Description",
        deprecated=True,
    ),
):
    return {"item": items[item_no]}

@app.post(
    "/items/{item_no}",
    tags=["items"],
    summary="create item summary",
)
async def create_item(
    item_id: int,
    item: Item = Body(..., embed=True),
):
    results = {"item_id": item_id, "item": item}
    return results

@app.get(
    "/users",
    tags=["users"],
)

async def read_users():
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    - FastAPIドキュメント反映テスト
    """
    return {"users": users}

@app.get(
    "/user/{user_no}",
    tags=["users"],
)
async def read_user(user_no: str):
    return {"user": users[user_no]}
