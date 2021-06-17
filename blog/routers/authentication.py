from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .. import database, models, token
from ..hashing import Hash
from sqlalchemy.orm import Session

router = APIRouter(tags=['Authentication'])
get_db = database.get_db


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=404, detail=f"Invalid Credentials xxxyyzz")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=404, detail=f"Incorrect password")

    access_token = token.create_access_token(data={'sub': user.email})
    return {"access_token": access_token, "token_type": "bearer"}
