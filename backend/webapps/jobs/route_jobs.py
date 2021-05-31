from fastapi import APIRouter, Request
from fastapi.params import Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.db.repository.jobs import list_jobs
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.db.repository.jobs import retrieve_job

templates = Jinja2Templates(directory="backend/templates")

router = APIRouter(
  prefix="",
  tags=["homepage"],
  include_in_schema=False
)

@router.get("/")
def home(request: Request, db: Session = Depends(get_db), msg:str = None):
  jobs = list_jobs(db=db)
  
  return templates.TemplateResponse("jobs/homepage.html", {"request": request, "jobs": jobs, "msg": msg})

@router.get("/detail/{id}")
def jobs_detail(id:int, request: Request, db: Session = Depends(get_db)):
  job = retrieve_job(id=id, db=db)
  return templates.TemplateResponse("jobs/detail.html",{"request": request, "job": job})