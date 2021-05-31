from fastapi import APIRouter, Request
from fastapi.params import Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import responses, status
from sqlalchemy.orm import Session
from fastapi.security.utils import get_authorization_scheme_param

from backend.db.models.users import User
from backend.db.repository.jobs import create_new_job  
from backend.db.session import get_db
from backend.db.repository.jobs import retrieve_job
from backend.webapps.jobs.forms import JobCreateForm
from backend.db.repository.jobs import list_jobs
from backend.apis.version1.route_login import get_current_user_from_token
from backend.schemas.jobs import JobCreate

templates = Jinja2Templates(directory="backend/templates")

router = APIRouter(
  prefix="",
  tags=["homepage"],
  include_in_schema=False
)

@router.get("/post-a-job/")  
def create_job(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("jobs/create_job.html", {"request": request})
 
 
@router.post("/post-a-job/")
async def create_job(request: Request, db: Session = Depends(get_db)):
    form = JobCreateForm(request)
    await form.load_data()
    if form.is_valid():
        try:
            token = request.cookies.get("access_token")
            scheme, param = get_authorization_scheme_param(
                token
            )  # scheme will hold "Bearer" and param will hold actual token value
            current_user: User = get_current_user_from_token(token=param, db=db)
            job = JobCreate(**form.__dict__)
            job = create_new_job(job=job, db=db, owner_id=current_user.id)
            return responses.RedirectResponse(
                f"/detail/{job.id}", status_code=status.HTTP_302_FOUND
            )
        except Exception as e:
            print(e)
            form.__dict__.get("errors").append(
                "You might not be logged in, In case problem persists please contact us."
            )
            return templates.TemplateResponse("jobs/create_job.html", form.__dict__)
    return templates.TemplateResponse("jobs/create_job.html", form.__dict__)

@router.get("/")
def home(request: Request, db: Session = Depends(get_db), msg:str = None):
  jobs = list_jobs(db=db)
  
  return templates.TemplateResponse("jobs/homepage.html", {"request": request, "jobs": jobs, "msg": msg})

@router.get("/detail/{id}")
def jobs_detail(id:int, request: Request, db: Session = Depends(get_db)):
  job = retrieve_job(id=id, db=db)
  return templates.TemplateResponse("jobs/detail.html",{"request": request, "job": job})

@router.get("/delete-job/")
def show_jobs_to_delete(request : Request, db : Session = Depends(get_db)):
    jobs = list_jobs(db=db)
    return templates.TemplateResponse("jobs/show_jobs_to_delete.html", {
        "request": request,
        "jobs": jobs
    })
