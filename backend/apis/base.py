from fastapi import APIRouter

from backend.apis.version1 import route_users, route_jobs, route_login

api_router = APIRouter()

api_router.include_router(route_login.router)
api_router.include_router(route_users.router)
api_router.include_router(route_jobs.router)
