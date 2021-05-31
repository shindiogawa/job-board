from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi import Request

router = APIRouter(
  include_in_schema=False,
  tags=["users"]
)

templates = Jinja2Templates(directory="backend/templates")

@router.get("/register/")
def register(request: Request):
  return templates.TemplateResponse("users/register.html", {"request": request})