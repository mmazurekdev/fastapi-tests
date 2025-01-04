import typing

import sqlalchemy
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.models.db.project import Project
from src.models.schemas.project import UpdateProjectSchema, CreateProjectSchema
from src.repository.crud.base import BaseCRUDRepository
from src.utilities.exceptions.database import EntityDoesNotExist


class ProjectCRUDRepository(BaseCRUDRepository):
    async def create_project(self, project_create: CreateProjectSchema) -> Project:
        new_project = Project(
            name=project_create.name,
            description=project_create.description,
            date_range_to=project_create.date_range_to,
            date_range_from=project_create.date_range_from,
            geo_file=project_create.geo_file.model_dump(),
        )
        self.async_session.add(instance=new_project)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_project)

        return new_project

    async def read_projects(self) -> typing.Sequence[Project]:
        stmt = sqlalchemy.select(Project)
        query = await self.async_session.execute(statement=stmt)
        return query.scalars().all()

    async def read_project_by_id(self, id: int) -> Project:
        stmt = sqlalchemy.select(Project).where(Project.id == id)
        query = await self.async_session.execute(statement=stmt)
        try:
            project = query.one()
            return project[0]
        except NoResultFound as x:
            raise EntityDoesNotExist(f"Project with id `{id}` does not exist!")

    async def update_project_by_id(
            self, id: int, project_update: UpdateProjectSchema
    ) -> Project:
        new_project_data = project_update.model_dump()

        select_stmt = sqlalchemy.select(Project).where(Project.id == id)
        query = await self.async_session.execute(statement=select_stmt)
        updated_project = query.scalar()

        if not updated_project:
            raise EntityDoesNotExist(f"Project with id `{id}` does not exist!")  # type: ignore

        update_stmt = (
            sqlalchemy.update(table=Project)
            .where(Project.id == updated_project.id)
            .values(updated_at=sqlalchemy_functions.now())
        )  # type: ignore
        update_stmt = update_stmt.values(geo_file=new_project_data["geo_file"])
        update_stmt = update_stmt.values(name=new_project_data["name"])
        update_stmt = update_stmt.values(
            date_range_to=new_project_data["date_range_to"]
        )
        update_stmt = update_stmt.values(
            date_range_from=new_project_data["date_range_from"]
        )
        update_stmt = update_stmt.values(description=new_project_data["description"])

        await self.async_session.execute(statement=update_stmt)
        await self.async_session.commit()
        await self.async_session.refresh(instance=updated_project)

        return updated_project  # type: ignore

    async def delete_project_by_id(self, id: int) -> str:
        select_stmt = sqlalchemy.select(Project).where(Project.id == id)
        query = await self.async_session.execute(statement=select_stmt)

        try:
            result = query.one()
            project = result[0]
            stmt = sqlalchemy.delete(table=Project).where(Project.id == project.id)

            await self.async_session.execute(statement=stmt)
            await self.async_session.commit()

            return f"Project with id '{id}' is successfully deleted!"
        except NoResultFound as x:
            raise EntityDoesNotExist(f"Project with id '{id}' does not exist!")  # type: ignore
