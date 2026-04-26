from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse 
from sqlmodel import Session, select
from database import get_session, engine 
from models import TaskLog, ActiveTimer  
from datetime import datetime 
import time

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    with Session(engine) as session:
        logs = session.exec(select(TaskLog).order_by(TaskLog.created_at.desc())).all()
        active_db = session.exec(select(ActiveTimer)).all()
        active_timers_dict = {t.task_name: t.start_time for t in active_db}
        
    stats = {}
    for log in logs:
        stats[log.date_str] = stats.get(log.date_str, 0) + (log.seconds / 3600)

    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={
            "logs": logs, 
            "stats": stats, 
            "active": active_timers_dict, # Folosim ce am citit din DB
            "now": datetime.now().strftime("%B %d, %Y")
        }
    )

@router.post("/start")
async def start_timer(task_name: str = Form(..., min_length=1)):
    task_name = task_name.strip()
    if not task_name:
        return RedirectResponse(url="/", status_code=303)
        
    with Session(engine) as session:
        new_timer = ActiveTimer(task_name=task_name, start_time=time.time())
        session.merge(new_timer) # merge face update dacă există deja sau insert dacă e nou
        session.commit()
        
    return RedirectResponse(url="/", status_code=303)

@router.post("/stop")
async def stop_timer(task_name: str = Form(...)):
    with Session(engine) as session:
        statement = select(ActiveTimer).where(ActiveTimer.task_name == task_name)
        timer = session.exec(statement).first()
        
        if timer:
            duration = int(time.time() - timer.start_time)
            session.add(TaskLog(name=task_name, seconds=duration))
            session.delete(timer) 
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