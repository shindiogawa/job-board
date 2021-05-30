from fastapi import APIRouter

from backend.apis.version1 import route_users, route_jobs

api_router = APIRouter()

api_router.include_router(route_users.router)
api_router.include_router(route_jobs.router)