from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, BackgroundTasks

from app.main import schemas,models
from app.main.core.i18n import translate
from app.main.core.security import decode_access_token


def get_db(request: Request) -> Generator:
    return request.state.db


class TokenRequired(HTTPBearer):

    def __init__(self, roles: list = [], auto_error: bool = False):
        self.roles = roles
        super(TokenRequired, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
        required_roles = self.roles
        credentials: HTTPAuthorizationCredentials = await super(TokenRequired, self).__call__(request)
        credentials_exception = HTTPException(status_code=401, detail=translate('invalid-credentials'),
                                              headers={"WWW-Authenticate": "Bearer"})
        if credentials:
            if not credentials.scheme == "Bearer":
                raise credentials_exception

            token_data = decode_access_token(credentials.credentials)
            if not token_data:
                raise credentials_exception

            user: models.User = db.query(models.User).filter(models.User.uuid == token_data['user_uuid']).first()
            if not user:
                raise credentials_exception
            
            if required_roles:
                if not self.verify_role(roles=required_roles, user=user):
                    raise HTTPException(status_code=403, detail=translate("not-authorized"))
                
            current_user = schemas.TokenData(
                uuid=user.uuid,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                role_uuid = user.role_uuid,
                role_title_fr = user.role_title_fr,
                role_title_en = user.role_title_en,
                role_code = user.role_code
            )

            return current_user

        else:
            raise HTTPException(status_code=401, detail=translate('invalid-credentials'))


    def verify_role(self, roles, user:models.User) -> bool:
        has_a_required_role = False
        if user.role_uuid:
            if isinstance(roles, str):
                if roles.lower() in [user.role_title_en.lower(), user.role_title_fr.lower()]:
                    has_a_required_role = True
            else:
                for role in roles:
                    if role.lower() in [user.role_title_en.lower(), user.role_title_fr.lower()]:
                        has_a_required_role = True
                        break
        return has_a_required_role
