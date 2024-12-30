from typing import Any,Dict
from app.main.core.config import Config
import emails,logging
from emails.templates import JinjaTemplate
import os
from pathlib import Path



@celery.task(name="send_email.task")
def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    assert Config.EMAILS_ENABLED, "aucune configuration fournie pour les variables de messagerie"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(Config.EMAILS_FROM_NAME, Config.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": Config.SMTP_HOST, "port": Config.SMTP_PORT}
    if Config.SMTP_TLS:
        smtp_options["tls"] = Config.SMTP_TLS
    if Config.SMTP_SSL:
        smtp_options["ssl"] = Config.SMTP_SSL
    if Config.SMTP_USER:
        smtp_options["user"] = Config.SMTP_USER
    if Config.SMTP_PASSWORD:
        smtp_options["password"] = Config.SMTP_PASSWORD

    print(message)
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"résultat de l'email envoyé: {response}")


def send_test_email(email_to: str) -> None:
    project_name = Config.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(Path(Config.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    task = send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": Config.PROJECT_NAME, "email": email_to},
    )
    # logging.info(f"new send mail task with id {task.id}")


def send_reset_password_email(email_to: str, token: str, name: str, prefered_language: str) -> None:
    server_host = Config.SERVER_HOST
    link = f"{server_host}/auth/reset-password"

    privacy_url = Config.PRIVACY_URL
    term_of_use_url = Config.TERM_OF_USE_URL

    if prefered_language in ['en', 'EN', 'en-EN']:
        subject = f"User password recovery"
        with open(Path(Config.EMAIL_TEMPLATES_DIR) / "reset_password_en.html") as f:
            template_str = f.read()

    else:
        subject = f"Récupération du mot de passe pour l'utilisateur"
        with open(Path(Config.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
            template_str = f.read()

    environment = {
       "code" : token,
       "email" : email_to,
       "valid_hours" : Config.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
       "link": link,
       "name": name,
       "privacy_url": privacy_url,
       "term_of_use_url": term_of_use_url
    }

    task = send_email(
        email_to=[email_to],
        subject_template=subject,
        html_template=template_str,
        environment=environment
    )
    # logging.info(f"new send mail task with id {task.id}")

# @celery.task(name="confirmation_create_account_mail")
# def confirmation_create_account_mail(
#     email_to: str, code: str, name: str, prefered_language: str,
#     is_professional: bool = False) -> None:

#     privacy_url = Config.PRIVACY_URL
#     term_of_use_url = Config.TERM_OF_USE_URL

#     if prefered_language in ['en', 'EN', 'en-EN']:
#         subject = f"Account creation validation"
#         with open(Path(Config.EMAIL_TEMPLATES_DIR) / "new_account_en.html") as f:
#             template_str = f.read()

#     else:
#         subject = f"Validation de création de compte"
#         with open(Path(Config.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
#             template_str = f.read()

#     environment = {
#        "code" : code,
#        "email" : email_to,
#        "valid_hours" : Config.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
#        "name": name,
#        "privacy_url": privacy_url,
#        "term_of_use_url": term_of_use_url,
#        "is_professional": is_professional
#     }

#     task = send_email(
#         email_to=[email_to],
#         subject_template=subject,
#         html_template=template_str,
#         environment=environment
#     )



# @celery.task(name="confirmation_account_creation_email")
# def confirmation_account_creation_email(
#     name: str, entreprise_phone: str,
#     phone: str, prefered_language: str,
#     entreprise_name: str, email_from:str,salon_uuid: str=None,
#     is_register: bool=True, password: str = None
# ) -> None:

#     payment_link = ""
#     if salon_uuid:
#         payment_link = Config.PAYMENT_LINK + salon_uuid

#     if prefered_language in ['en', 'EN', 'en-EN']:
#         subject = f"Account confirmation for Carla+ Curls" if is_register else "Account creation on Carla+ Curls"
#         with open(Path(Config.EMAIL_TEMPLATES_DIR) / "confirmation_account_creation_email_en.html") as f:
#             template_str = f.read()
#     else:
#         subject = f"Confirmation du compte de Carla+ Curls" if is_register else "Création de compte sur Carla+ Curls"
#         with open(Path(Config.EMAIL_TEMPLATES_DIR) / "confirmation_account_creation_email.html") as f:
#             template_str = f.read()

#     environment = {
#        "name": name,
#        "email_from": email_from,
#        "phone": phone,
#        "payment_link": payment_link,
#        "entreprise_name": entreprise_name,
#        "entreprise_phone": entreprise_phone,
#        "is_register": is_register,
#        "password": password
#     }

#     if is_register:
#         for email in Config.contact_emails:

#             task = send_email(
#                 email_to=[email],
#                 subject_template=subject,
#                 html_template=template_str,
#                 environment=environment
#             )
#     else:
#         task = send_email(
#             email_to=[email_from],
#             subject_template=subject,
#             html_template=template_str,
#             environment=environment
#         )
#     # logging.info(f"new send mail task with id {task.id}")
