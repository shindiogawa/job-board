from fastapi import APIRouter, Request
from fastapi.params import Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.db.repository.jobs import list_jobs
from sqlalchemy.orm import Session
from backend.db.session import get_db
templates = Jinja2Templates(directory="backend/templates")

router = APIRouter(
  prefix="",
  tags=["homepage"],
  include_in_schema=False
)

@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
  jobs = list_jobs(db=db)
  
  return templates.TemplateResponse("jobs/homepage.html", {"request": request, "jobs": jobs})