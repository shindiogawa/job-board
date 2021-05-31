from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.templating import Jinja2Templates

from starlette.requests import Request
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.webapps.auth.forms import LoginForm
from backend.apis.version1.route_login import login_for_access_token


templates = Jinja2Templates(directory="backend/templates")
router = APIRouter(include_in_schema=False)

@router.get("/login/")
def login(request: Request):
  return templates.TemplateResponse("auth/login.html", {"request": request})

@router.post("/login/")
async def login(request: Request, db: Session = Depends(get_db)):
  form = LoginForm(request=request)

  await form.load_data()

  if await form.is_valid():
    try:
      form.__dict__.update(msg="Login Successfully :)")
      response = templates.TemplateResponse("auth/login.html", form.__dict__)
      login_for_access_token(response=response, form_data=form, db=db)
      return response
    except HTTPException:
      form.__dict__update(msg="")
      form.__dict__.get("errors").append("Incorrect email or password")
      return templates.TemplateResponse("auth/login.html", form.__dict__)

  return templates.TemplateResponse("auth/login.html", form.__dict__)