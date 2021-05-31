from fastapi import APIRouter

from backend.webapps.jobs import route_jobs
from backend.webapps.users import route_users
from backend.webapps.auth import route_login

api_router = APIRouter()

api_router.include_router(route_jobs.router)
api_router.include_router(route_users.router)
api_router.include_router(route_login.router)
