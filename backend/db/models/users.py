from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import foreign
from sqlalchemy.sql.schema import Column

from db.base_class import Base

class User(Base):
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, nullable=False, unique=True)
  email = Column(String, nullable=False, unique=True, index=True)
  hashed_password = Column(String, nullable=False)
  is_active =  Column(Boolean(), default= True)
  is_superuser = Column(Boolean(), default=False)
  jobs = relationship("Job", back_populates="owner")
 
