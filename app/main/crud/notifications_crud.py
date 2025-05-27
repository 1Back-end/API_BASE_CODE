from datetime import date
from fastapi import BackgroundTasks, HTTPException
from app.main.core.i18n import __
from app.main.core.mail import send_notification_to_candidate
from sqlalchemy.orm import Session
from app.main import models,schemas
from jinja2 import Template
from app.main.core.config import Config


@classmethod

def send_notification_to_candidate(email: str, name:str , job_title: str, job_description: str):

# Récupérer tous les candidats inscrits dans le système
candidates = db.query(models.Candidat).filter(models.Candidat.is_deleted==False).all()

        
for candidate in candidates:
            background_tasks.add_task(
                send_notification_to_candidate, 
                email=candidate.email, 
                name=f"{candidate.first_name} {candidate.last_name}", 
                job_title=offers.title, 
                job_description=offers.description
            
            )
        # Retourner l'offre créée
        return msg 
    