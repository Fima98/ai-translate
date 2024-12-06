from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    tags=["Profile"]
)


@router.get('/me', response_model=schemas.User)
def get_current_user(db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    user_data = db.query(models.User).filter(
        models.User.id == user.id).first()

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user.id} does not exist"
        )

    return user_data
