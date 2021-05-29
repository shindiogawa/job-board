from sqlalchemy.orm import Session

from backend.schemas.jobs import JobCreate
from backend.db.models.jobs import Job


def create_new_job(job: JobCreate, db: Session, owner_id: int):
  job = Job(**job.dict(), owner_id= owner_id)
  db.add(job)
  db.commit()
  db.refresh(job)
  return job