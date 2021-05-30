from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, session

from backend.db.session import get_db
from backend.db.models.jobs import Job
from backend.schemas.jobs import JobCreate, ShowJob
from backend.db.repository.jobs import create_new_job, delete_job_by_id, retrieve_job, list_jobs, update_job_by_id

router = APIRouter(
    prefix="/job",
  tags=["jobs"]
)

@router.post("/create-job", response_model=ShowJob)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
  owner_id = 1
  job = create_new_job(job=job, db=db, owner_id=owner_id)
  return job

@router.get("/get/{id}", response_model=ShowJob)
def retrieve_job_by_id(id:int, db: Session = Depends(get_db)):
  job = retrieve_job(id=id, db=db)
  if not job:
    raise HTTPException(  status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Job with id {id} does not exist"
                  )
  return job

@router.get("/all", response_model=List[ShowJob])
def retrieve_all_jobs(db:Session = Depends(get_db)):
  jobs = list_jobs(db=db)
  return jobs

@router.put("/update/{id}")
def update_job(id: int, job:JobCreate, db: Session=Depends(get_db)):
  owner_id = 1
  message = update_job_by_id(id=id, job=job, db=db, owner_id=owner_id)
  if not message:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    detail= f"Job with id {id} does not exist")
  return {"detail": "Successfully updated data."}

@router.delete("/delete/{id}")
def delete_job(id:int, db: Session =Depends(get_db)):
  owner_id = 1
  message = delete_job_by_id(id=id, db=db, owner_id=owner_id)
  if not message:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    detail= f"Job with id {id} does not exist")
  return {"detail": "Successfully deleted the job."}