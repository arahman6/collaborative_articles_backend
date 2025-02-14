from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import db  
from seed_data import seed_data  
from routers import router  

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up... checking for initial data")
    await seed_data()
    yield  # This allows the app to continue running
    print("Shutting down... closing resources")

app = FastAPI(lifespan=lifespan)

app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to Collaborative Articles Backend!"}
