from fastapi import Depends, HTTPException, status, APIRouter, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2, database
from ..database import get_db


router = APIRouter(
    tags=["Authorize"]
)


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.User, tags=["Authentication"])
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = oauth2.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), response: Response = Response(), db: Session = Depends(database.get_db)):
    if not user_credentials.username or not user_credentials.password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid Credentials"
        )

    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not oauth2.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    # ACCESS_TOKEN TO COOKIE
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=False,  # Захист від XSS
        secure=True,    # Використовуйте True для HTTPS
        samesite="Lax"  # Захист від CSRF
    )

    return {"access_token": access_token, "token_type": "bearer"}
