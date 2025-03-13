from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.articles import articles_router
from app.routers.users import users_router
from app.routers.contributions import contributions_router
from app.routers.comments import comments_router
from app.routers.admin import admin_router
import os
import boto3

def get_secret():
    ssm_client = boto3.client("ssm", region_name="us-east-1")  # Ensure correct region
    response = ssm_client.get_parameter(Name="/fastapi/jwt_secret_key", WithDecryption=True)
    return response["Parameter"]["Value"]

# Fetch the secret dynamically
JWT_SECRET_KEY = get_secret()


app = FastAPI()
# app = FastAPI(
#     title="Collaborative Articles API",
#     description="A FastAPI backend for AI-generated and user-contributed articles.",
#     version="1.0.0",
#     contact={
#         "name": "Arif Rahman",
#         "email": "arahman@gmail.com",
#         "url": "https://github.com/arahman6/collaborative_articles_backend"
#     },
#     license_info={
#         "name": "MIT License",
#         "url": "https://opensource.org/licenses/MIT",
#     }
# )

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(articles_router, prefix="/api/v1/articles", tags=["Articles"])
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(contributions_router, prefix="/api/v1", tags=["Contributions"])
app.include_router(comments_router, prefix="/api/v1", tags=["Comments"])
app.include_router(admin_router, prefix="/api/v1/admin", tags=["Admin"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Collaborative Articles API"}

