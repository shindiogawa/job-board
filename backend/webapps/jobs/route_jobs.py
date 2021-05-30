from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="backend/templates")

router = APIRouter(
  prefix="",
  tags=["homepage"],
  include_in_schema=False
)

@router.get("/")
def home(request: Request):
  dir(request)
  
  return templates.TemplateResponse("jobs/homepage.html", {"request": request})