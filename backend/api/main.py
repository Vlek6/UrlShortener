from api.routes import url
from fastapi import APIRouter
from fastapi.responses import JSONResponse

api_router = APIRouter()


@api_router.get("/", status_code=200)
def root() -> JSONResponse:
    return JSONResponse(content={"message": "Working URL Shortener app"})


@api_router.get("/healtcheck", status_code=200)
def healthcheck() -> JSONResponse:
    return JSONResponse(content={"status": "healthy"})


# Add external routers
api_router.include_router(url.router, prefix="/url", tags=["url"])
