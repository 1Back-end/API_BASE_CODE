from datetime import date
from fastapi import BackgroundTasks, HTTPException
from fastapi import APIRouter, Depends, Body, Query
from app.main.core.i18n import __
from app.main.core.mail import send_notification_to_candidate
from sqlalchemy.orm import Session
from app.main import models,schemas
from jinja2 import Template
from app.main.core.config import Config

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.post("/send",response_model=schemas.Msg)
def send_notifications(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.CandidateCreate,
    background_tasks: BackgroundTasks,
    current_candidates: models.candidates = Depends(TokenRequired(roles=["CANDIDATES"])),  
):
    crud.notifications.send(db=db,obj_in=obj_in,background_tasks=background_tasks)
    return schemas.Msg(message=__(key="notifications-sent-successfully"))
