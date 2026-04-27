from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from database import init_db
from routes.routes import router  
app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(router)