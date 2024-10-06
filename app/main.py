from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from core.auth import authenticate_user, create_access_token, get_current_user, get_user_role
from core.db import async_session
from core.schemas import *
from core.crud import *


# Create FastAPI instance
app = FastAPI()

# Dependency to get the database session
async def get_db():
    async with async_session() as session:
        yield session

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await create_user(db=db, user=user)

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user

@app.get("/admin/", response_model=str)
async def read_admin_data(current_user: schemas.User = Depends(get_current_user), role: str = Depends(get_user_role)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")
    return "This is the admin data"
