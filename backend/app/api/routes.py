from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from backend.app.db.session import get_session
from backend.app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from backend.app.crud import project as project_crud

router = APIRouter(prefix="/api")


@router.get("/health")
async def health_check():
    return {"status": "healthy"}


@router.post("/projects", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    db: AsyncSession = Depends(get_session)
):
    """Create a new project"""
    return await project_crud.create_project(db, project)


@router.get("/projects", response_model=List[ProjectResponse])
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_session)
):
    """List all projects"""
    return await project_crud.get_projects(db, skip=skip, limit=limit)


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_session)
):
    """Get project by ID"""
    project = await project_crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: AsyncSession = Depends(get_session)
):
    """Update a project"""
    updated_project = await project_crud.update_project(db, project_id, project)
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated_project


@router.delete("/projects/{project_id}")
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_session)
):
    """Delete a project"""
    success = await project_crud.delete_project(db, project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"status": "success", "message": "Project deleted"}

