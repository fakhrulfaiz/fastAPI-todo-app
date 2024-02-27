from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, Path, APIRouter, Request, Form
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from routers import auth
from database import SessionLocal
import models
from models import Todos, Users
from .auth import get_current_user

router = APIRouter(
    prefix='/users',
    tags=['users']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

templates = Jinja2Templates("template")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Authentication Failed.')
    return db.query(Users).filter(Users.id == user.get('id')).first()


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


@router.get("/password")
async def change_password_page(request: Request):
    return templates.TemplateResponse("change-password.html", {"request": request})


@router.post("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(request: Request, db: db_dependency,
                          username: str = Form(...), password: str = Form(...), newpassword: str = Form(...),
                          newpassword2: str = Form(...)):

    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    user_model = db.query(Users).filter(Users.username == username).first()

    if not bcrypt_context.verify(password, user_model.hashed_password):
        msg = "Enter your password correctly"
        return templates.TemplateResponse("change-password.html", {"request": request, "msg": msg})

    if not newpassword == newpassword2:
        msg = "New Password must be same"
        return templates.TemplateResponse("change-password.html", {"request": request, "msg": msg})

    user_model.hashed_password = bcrypt_context.hash(newpassword)
    db.add(user_model)
    db.commit()
    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


@router.put("/phonenumber", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(phone_num: str, user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Authentication Failed.')

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_num

    db.add(user_model)
    db.commit()

