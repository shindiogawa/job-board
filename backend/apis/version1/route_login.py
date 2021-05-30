from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends
from fastapi import APIRouter
from rsa import key
from sqlalchemy.orm import Session
from datetime import timedelta
from backend.db.session import get_db
from backend.core.config import settings
from backend.core.security import create_access_token
from backend.db.repository.login import get_user
from backend.core.hashing import Hasher
from jose import jwt, JWTError
router = APIRouter(
  prefix="/login",
  tags=["login"]
)

def authenticate_user(username: str, password: str, db: Session):
  user = get_user(username=username, db=db)
  print(user)
  if not user:
    return False
  if not Hasher.verify_password(password, user.hashed_password):
    return False
  return user

@router.post("/token")
def login_for_access_token(form_data:OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):
  user = authenticate_user(form_data.username, form_data.password, db)
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="Incorrect username or password")
  access_token_expire = timedelta(minutes = settings.ACCESS_TOKEN_EXPIRES_MINUTE)
  access_token = create_access_token(data = {"sub": user.email}, expires_delta = access_token_expire)
  return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


def get_current_user_from_token(
  token: str = Depends(oauth2_scheme), 
  db: Session = Depends(get_db)):

  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials"
  )

  try:
    payload = jwt.decode(
      token, 
      settings.SECRET_KEY, 
      algorithms=[settings.ALGORITHM]
    )
    username: str = payload.get("sub")
    print("email is", username)
    if username is None:
      raise credentials_exception

  except JWTError:
    raise credentials_exception

  user = get_user(username=username, db=db)

  if user is None:
    raise credentials_exception
  return user



    