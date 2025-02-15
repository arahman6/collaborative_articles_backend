from fastapi import FastAPI
from app.routers.articles import articles_router
from app.routers.users import users_router
from app.routers.contributions import contributions_router
from app.routers.comments import comments_router
import os
import boto3

def get_secret():
    ssm_client = boto3.client("ssm", region_name="us-east-1")  # Ensure correct region
    response = ssm_client.get_parameter(Name="/fastapi/jwt_secret_key", WithDecryption=True)
    return response["Parameter"]["Value"]

# Fetch the secret dynamically
JWT_SECRET_KEY = get_secret()


app = FastAPI()

# Include all routers
app.include_router(articles_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(contributions_router, prefix="/api/v1")
app.include_router(comments_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the Collaborative Articles API"}

