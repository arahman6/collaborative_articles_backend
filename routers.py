from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from database import db
from models import Article, Contribution, User, Comment
from datetime import datetime, timezone
from bson import ObjectId
from passlib.context import CryptContext

router = APIRouter()

@router.post("/articles/", response_model=Article)
async def create_article(article: Article):
    article_data = article.model_dump()
    article_data["created_at"] = datetime.now(timezone.utc).isoformat()
    article_data["updated_at"] = article_data["created_at"]
    result = await db["articles"].insert_one(article_data)
    article_data["_id"] = result.inserted_id
    return article_data



@router.get("/articles/")
async def list_articles(sector: str = None):
    query = {} if not sector else {"sector": sector}
    articles = await db["articles"].find(query).to_list(100)

    for article in articles:
        article["_id"] = str(article["_id"])

    return jsonable_encoder(articles)

@router.get("/articles/{id}/")
async def get_article(id: str):
    article = await db["articles"].find_one({"_id": ObjectId(id)})
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    article["_id"] = str(article["_id"])
    return jsonable_encoder(article)


@router.post("/articles/{id}/contribute/", response_model=Contribution)
async def add_contribution(id: str, contribution: Contribution):
    contribution_data = contribution.model_dump()
    contribution_data["article_id"] = id
    contribution_data["created_at"] = datetime.now(timezone.utc).isoformat()
    result = await db["contributions"].insert_one(contribution_data)
    contribution_data["_id"] = result.inserted_id
    return contribution_data


@router.get("/articles/{id}/contributions/")
async def list_contributions(id: str):
    contributions = await db["contributions"].find({"article_id": id}).to_list(100)
    return contributions



# Password hashing utility
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/users/register/")
async def register_user(user: User):
    user_data = user.model_dump()
    user_data["hashed_password"] = pwd_context.hash(user.hashed_password)
    del user_data["hashed_password"]  # Save only hashed password
    result = await db["users"].insert_one(user_data)
    user_data["_id"] = result.inserted_id
    return {"message": "User registered successfully", "user_id": str(user_data["_id"])}


@router.post("/users/login/")
async def login_user(email: str, password: str):
    user = await db["users"].find_one({"email": email})
    if not user or not pwd_context.verify(password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # Generate JWT (add actual JWT generation here)
    return {"message": "Login successful"}



@router.post("/articles/{id}/comments/")
async def add_comment(id: str, comment: Comment):
    comment_data = comment.model_dump()
    comment_data["article_id"] = id
    comment_data["created_at"] = datetime.now(timezone.utc).isoformat()
    result = await db["comments"].insert_one(comment_data)
    comment_data["_id"] = result.inserted_id
    return comment_data


@router.get("/articles/{id}/comments/")
async def list_comments(id: str):
    comments = await db["comments"].find({"article_id": id}).to_list(100)
    return comments
