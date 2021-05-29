from sqlalchemy.orm import Session

from backend.schemas.users import UserCreate
from backend.db.models.users import User
from backend.core.hashing import Hasher

def create_new_user(user: UserCreate, db: Session):
  user = User(
    username= user.username, 
    email= user.email,
    
     )