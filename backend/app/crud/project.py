from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from backend.app.models.project import Project
from backend.app.schemas.project import ProjectCreate, ProjectUpdate


async def create_project(db: AsyncSession, project: ProjectCreate) -> Project:
    """Create a new project"""
    db_project = Project(
        name=project.name,
        description=project.description
    )
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project


async def get_project(db: AsyncSession, project_id: int) -> Optional[Project]:
    """Get project by ID"""
    result = await db.execute(select(Project).where(Project.id == project_id))
    return result.scalar_one_or_none()


async def get_projects(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Project]:
    """Get all projects with pagination"""
    result = await db.execute(select(Project).offset(skip).limit(limit))
    return result.scalars().all()


async def update_project(db: AsyncSession, project_id: int, project: ProjectUpdate) -> Optional[Project]:
    """Update a project"""
    db_project = await get_project(db, project_id)
    if not db_project:
        return None
    
    if project.name is not None:
        db_project.name = project.name
    if project.description is not None:
        db_project.description = project.description
    
    await db.commit()
    await db.refresh(db_project)
    return db_project


async def delete_project(db: AsyncSession, project_id: int) -> bool:
    """Delete a project"""
    db_project = await get_project(db, project_id)
    if not db_project:
        return False
    
    await db.delete(db_project)
    await db.commit()
    return True

