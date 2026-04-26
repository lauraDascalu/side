from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from database import init_db, get_session
from routes.routes import router
from sqlmodel import Session, select
from models import TaskLog
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")
@app.on_event("startup")
def on_startup():
    init_db()
app.include_router(router)

