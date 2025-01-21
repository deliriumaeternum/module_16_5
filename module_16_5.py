from fastapi import FastAPI, Path, HTTPException, Request
from typing import Annotated, List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)
templates = Jinja2Templates(directory="templates")

users = []

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get("/")
async def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get("user/{user_id}")
async def get_users(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id]})
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')

@app.post("/user/{username}/{age}")
async def create_user(
        username: Annotated[str, Path(min_length=3, max_length=15, description='Enter username', example='UrbanUser')],
        age: Annotated[int, Path(ge=14, le=100, description='Enter age', example='18')]) -> User:
    user_id = max((i.id for i in users), default=0) + 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
        user_id: Annotated[int, Path(min_length=1, max_length=15, description='Enter user_id', example='1')],
        username: Annotated[str, Path(min_length=3, max_length=15, description='Enter username', example='UrbanUser')],
        age: Annotated[int, Path(ge=14, le=100, description='Enter age', example='18')]) -> User:
    for i in users:
        if i.id == user_id:
            i.username = username
            i.age = age
            return i
    raise HTTPException(status_code=404, detail='User was not found')

@app.delete("/user/{user_id}")
async def delete_user(
        user_id: Annotated[int, Path(min_length=1, max_length=15, description='Enter user_id', example='1')]) -> User:
    for k, i in enumerate(users):
        if i.id == user_id:
            return users.pop(k)
    raise HTTPException(status_code=404, detail='User was not found')