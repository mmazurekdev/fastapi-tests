import fastapi

from src.api.routes.project import router as project_router

router = fastapi.APIRouter()

router.include_router(router=project_router)
