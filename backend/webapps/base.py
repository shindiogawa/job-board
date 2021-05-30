from fastapi import APIRouter

from backend.webapps.jobs import route_jobs

api_router = APIRouter()

api_router.include_router(route_jobs.router)

