from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.db.session import get_session
from backend.app.models.user import User
from backend.app.core.security import verify_password, hash_password, create_access_token

router = APIRouter(prefix="/auth")

@router.post("/register")
async def register(username: str, password: str, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).where(User.username == username))
    if result.scalar():
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(username=username, password_hash=hash_password(password))
    db.add(user)
    await db.commit()
    return {"msg": "User registered"}

@router.post("/login")
async def login(username: str, password: str, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

