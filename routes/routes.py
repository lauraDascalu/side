from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse 
from sqlmodel import Session, select
from database import get_session, engine 
from models import TaskLog
from datetime import datetime 
import time

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

router = APIRouter()
active_timers = {}

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    with Session(engine) as session:
        logs = session.exec(select(TaskLog).order_by(TaskLog.created_at.desc())).all()
    
    stats = {}
    for log in logs:
        stats[log.date_str] = stats.get(log.date_str, 0) + (log.seconds / 3600)

    return templates.TemplateResponse(
    request=request, 
    name="index.html", 
    context={
        "logs": logs, 
        "stats": stats, 
        "active": active_timers,
        "now": datetime.now().strftime("%B %d, %Y")
    }
)

@router.post("/start")
async def start_timer(task_name: str = Form(..., min_length=1)):
    # Curățăm textul de spații goale inutile (ex: "  ")
    task_name = task_name.strip()
    if not task_name:
        return RedirectResponse(url="/", status_code=303)
        
    active_timers[task_name] = time.time()
    return RedirectResponse(url="/", status_code=303)

@router.post("/stop")
async def stop_timer(task_name: str = Form(...)):
    if task_name in active_timers:
        duration = int(time.time() - active_timers.pop(task_name))
        with Session(engine) as session:
            session.add(TaskLog(name=task_name, seconds=duration))
            session.commit()
    return RedirectResponse(url="/", status_code=303)

@router.post("/delete/{task_id}")
async def delete_task(task_id: int):
    with Session(engine) as session:
        task = session.get(TaskLog, task_id)
        if task:
            session.delete(task)
            session.commit()
    return RedirectResponse(url="/", status_code=303)