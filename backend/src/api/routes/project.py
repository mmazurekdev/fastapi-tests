import fastapi

from src.api.dependencies.repository import get_repository
from src.models.schemas.project import (
    ResponseProjectSchema,
    UpdateProjectSchema,
    CreateProjectSchema,
)
from src.repository.crud.project import ProjectRepository
from src.utilities.exceptions.database import EntityDoesNotExist

router = fastapi.APIRouter(prefix="/projects", tags=["projects"])


@router.get(
    path="",
    name="projects:read-projects",
    response_model=list[ResponseProjectSchema],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_projects(
    projects_repo: ProjectRepository = fastapi.Depends(
        get_repository(repo_type=ProjectRepository)
    ),
) -> list[ResponseProjectSchema]:
    projects = await projects_repo.read_projects()
    response = []
    for project in projects:
        response.append(
            ResponseProjectSchema(
                id=project.id,
                name=project.name,
                description=project.description,
                date_range_to=project.date_range_to,
                date_range_from=project.date_range_from,
                geo_file=project.geo_file,
            )
        )
    return response


@router.get(
    path="/{id}",
    name="projects:read-project-by-id",
    response_model=ResponseProjectSchema | None,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_project(
    id: int,
    response: fastapi.Response,
    projects_repo: ProjectRepository = fastapi.Depends(
        get_repository(repo_type=ProjectRepository)
    ),
) -> ResponseProjectSchema | None:
    try:
        project = await projects_repo.read_project_by_id(id=id)
        return ResponseProjectSchema(
            id=project.id,
            name=project.name,
            description=project.description,
            date_range_to=project.date_range_to,
            date_range_from=project.date_range_from,
            geo_file=project.geo_file,
        )
    except EntityDoesNotExist:
        response.status_code = fastapi.status.HTTP_404_NOT_FOUND
        return


@router.put(
    path="/{id}",
    name="projects:update-project-by-id",
    response_model=ResponseProjectSchema,
    status_code=fastapi.status.HTTP_200_OK,
)
async def update_account(
    id: int,
    project_update: UpdateProjectSchema,
    response: fastapi.Response,
    project_repo: ProjectRepository = fastapi.Depends(
        get_repository(repo_type=ProjectRepository)
    ),
) -> ResponseProjectSchema | None:
    try:
        project = await project_repo.update_project_by_id(
            id=id, project_update=project_update
        )
        return ResponseProjectSchema(
            id=project.id,
            name=project.name,
            description=project.description,
            date_range_to=project.date_range_to,
            date_range_from=project.date_range_from,
            geo_file=project.geo_file,
        )
    except EntityDoesNotExist:
        response.status_code = fastapi.status.HTTP_404_NOT_FOUND
        return


@router.delete(
    path="/{id}",
    name="projects:delete-project-by-id",
    status_code=fastapi.status.HTTP_200_OK,
)
async def delete_account(
    id: int,
    response: fastapi.Response,
    project_repo: ProjectRepository = fastapi.Depends(
        get_repository(repo_type=ProjectRepository)
    ),
) -> str | None:
    try:
        deletion_result = await project_repo.delete_project_by_id(id=id)
        return deletion_result

    except EntityDoesNotExist:
        response.status_code = fastapi.status.HTTP_404_NOT_FOUND
        return


@router.post(
    path="", name="projects:create_project", status_code=fastapi.status.HTTP_200_OK
)
async def create_project(
    new_project_data: CreateProjectSchema,
    projects_repo: ProjectRepository = fastapi.Depends(
        get_repository(repo_type=ProjectRepository)
    ),
) -> ResponseProjectSchema:
    project = await projects_repo.create_project(new_project_data)
    return ResponseProjectSchema(
        id=project.id,
        name=project.name,
        description=project.description,
        date_range_to=project.date_range_to,
        date_range_from=project.date_range_from,
        geo_file=project.geo_file,
    )
