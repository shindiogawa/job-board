from fastapi import APIRouter, responses
from fastapi.param_functions import Depends
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.db.repository.users import create_new_user
from backend.schemas.users import UserCreate
from backend.webapps.users.forms import UserCreateForm
from backend.db.session import get_db



router = APIRouter(
  include_in_schema=False,
  tags=["users"]
)

templates = Jinja2Templates(directory="backend/templates")

@router.get("/register/")
def register(request: Request):
  return templates.TemplateResponse("users/register.html", {"request": request})

@router.post("/register/")
async def register(request: Request, db : Session = Depends(get_db)):
  form = UserCreateForm(request)
  await form.load_data()
  if await form.is_valid():
    user = UserCreate(username=form.username, email = form.email, password = form.password)
    try:
      user = create_new_user(user = user, db = db)
      return responses.RedirectResponse("/", status_code =  status.HTTP_302_FOUND)
    except IntegrityError:
      form.__dict__.get("errors").append("Duplicate username or email")
      return templates.TemplateResponse("users/register.html", form.__dict__)
  return templates.TemplateResponse("users/register.html", form.__dict__)
    