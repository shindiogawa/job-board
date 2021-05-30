from sqlalchemy.orm import Session
from backend.db.models.users import User

def get_user(username:str, db:Session):
  user = db.query(User).filter(User.email == username)
  return user.first()