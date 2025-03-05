Collaborative Articles API
==========================

**Collaborative Articles API** is a robust and modular serverless FastAPI backend that empowers users to collaboratively create, manage, and engage with AI-generated articles. Built with scalability and advanced OOP design in mind, the API offers a rich set of features including secure user authentication, role-based access control, AI-driven article generation, real-time engagement analytics, gamification with badges & achievements, and a dedicated admin dashboard for content moderation and insights. The project is deployed on AWS Lambda and API Gateway using AWS SAM.

Key Features
---------------

-   **AI-Generated Content**: Automatically generate detailed articles on various topics (Tech, Health, Corporate, Politics, Youth, Lifestyle) using OpenAI.
-   **Secure Authentication & JWT**: Register, login, and manage sessions using robust JWT authentication.
-   **Role-Based Access Control (RBAC)**: Granular permissions for admins, contributors, and readers to control access to features.
-   **Article Management**: Create, update, delete, and track contributions to articles.
-   **Comment System**: Enable discussions with full CRUD operations and moderation capabilities.
-   **User Activity & Engagement Analytics**: Monitor views, comments, and overall engagement in real time.
-   **Gamification**: Earn badges and achievements based on activity to foster engagement.
-   **Admin Dashboard**: Powerful tools for content moderation, user management, and analytics.
-   **Serverless Deployment**: Easily deployable using AWS Lambda, API Gateway, and AWS SAM.

Project Structure
--------------------

```
app/
├── models/                   # Pydantic models for data validation
│   ├── base.py               # Base model with common fields
│   ├── user.py               # User model and related sub-models
│   ├── article.py            # Article model
│   ├── comment.py            # Comment model
│   ├── contribution.py       # Contribution model
│   └── ...                   # Additional models as needed
├── database/                 # Database access layer (MongoDB)
│   ├── db.py                 # MongoDB connection and initialization
│   ├── user_repository.py    # User database operations
│   ├── article_repository.py # Article operations (including bulk insert)
│   ├── comment_repository.py # Comment operations
│   ├── contribution_repository.py  # Contribution tracking
│   ├── engagement_analytics_repository.py  # Engagement metrics
│   ├── badge_repository.py    # Badge assignment and retrieval
│   ├── admin_repository.py    # Admin moderation and user management
│   └── ...                   # Additional repositories as needed
├── routers/                  # API endpoints (routes)
│   ├── users.py              # User authentication, signup, profile management
│   ├── articles.py           # Article CRUD and AI-generated articles
│   ├── comments.py           # Comment CRUD operations
│   ├── contributions.py      # Contribution tracking
│   ├── engagement_analytics.py # Engagement analytics endpoints
│   ├── badges.py             # Badge and achievement endpoints
│   ├── admin.py              # Admin dashboard and moderation APIs
│   └── ...                   # Additional routers as needed
├── services/                 # Business logic and external integrations
│   ├── auth_service.py       # Authentication and JWT handling
│   ├── openai_service.py     # OpenAI integration for article generation
│   ├── article_generator_service.py  # AI-based article generation workflow
│   └── ...                   # Additional services as needed
├── roles/                    # Role-based access control implementations
│   ├── role_interface.py     # Abstract role interface
│   ├── admin.py              # Admin role definition
│   ├── contributor.py        # Contributor role definition
│   ├── reader.py             # Reader role definition
│   └── role_factory.py       # Factory to get role instances
├── tasks/                    # Background tasks (if needed)
├── utils/                    # Utility functions and helpers
├── main.py                   # FastAPI application entry point
├── config.py                 # Configuration & environment variables
├── seed_data.py              # Data seeding scripts
└── ...

```

## Installation & Setup
### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/collaborative_articles_backend.git
cd collaborative_articles_backend/fastapi-sam
```
### **2. Set Up Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

## Running Locally
Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
Access the API documentation at:
- **Swagger UI** → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc** → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Running Tests
Run all unit & integration tests:
```bash
pytest tests/
```

## Deploying to AWS
### **1. Install AWS SAM CLI**
```bash
brew install aws-sam-cli  # macOS
choco install aws-sam-cli  # Windows
```
### **2️. Build the Lambda Package**
```bash
sam build
```
### **3. Deploy to AWS**
```bash
sam deploy --guided
```
### **4. Get the API Gateway URL**
After deployment, AWS will provide an API Gateway URL, e.g.:
```
FastAPIEndpoint: https://xyz123.execute-api.us-east-1.amazonaws.com/Prod/
```
Test the API:
```bash
curl https://xyz123.execute-api.us-east-1.amazonaws.com/Prod/api/v1/articles/
```

## Authentication & JWT
- Users can **signup & login** using JWT authentication.
- JWT secret is stored in **AWS SSM Parameter Store** for security.

## API Endpoints

### Articles
| Method | Endpoint                           | Description                                              |
|--------|------------------------------------|----------------------------------------------------------|
| POST   | `/api/v1/articles/`                | Create a new article (Admins/Contributors only)          |
| GET    | `/api/v1/articles/`                | Retrieve all articles                                    |
| GET    | `/api/v1/articles/{id}`            | Retrieve a single article by ID                          |
| PUT    | `/api/v1/articles/{id}`            | Update an article (Admins/Contributors only)             |
| DELETE | `/api/v1/articles/{id}`            | Delete an article (Admins only)                          |
| POST   | `/api/v1/articles/generate/`       | Generate AI-based articles (Admins only)                 |

### Users
| Method | Endpoint                          | Description                                             |
|--------|-----------------------------------|---------------------------------------------------------|
| POST   | `/api/v1/signup/`                 | Register a new user                                     |
| POST   | `/api/v1/login/`                  | User login & JWT token generation                       |
| GET    | `/api/v1/profile/`                | Get the authenticated user's profile                    |
| PUT    | `/api/v1/profile/`                | Update user profile                                     |
| PUT    | `/api/v1/change-password/`        | Change user password                                    |
| DELETE | `/api/v1/delete-account/`         | Delete user account                                     |

### Contributions
| Method | Endpoint                                     | Description                                               |
|--------|----------------------------------------------|-----------------------------------------------------------|
| POST   | `/api/v1/contributions/{article_id}`         | Log a contribution for a specific article               |
| GET    | `/api/v1/contributions/user/{user_id}`         | Get all contributions made by a user                      |
| GET    | `/api/v1/contributions/article/{article_id}`   | Get all contributions for a specific article              |

### Comments
| Method | Endpoint                                     | Description                                              |
|--------|----------------------------------------------|----------------------------------------------------------|
| POST   | `/api/v1/comments/{article_id}`               | Add a comment to an article                              |
| GET    | `/api/v1/comments/{article_id}`               | Retrieve all comments for an article                     |
| PUT    | `/api/v1/comments/{comment_id}`               | Update a comment (only the owner can update)             |
| DELETE | `/api/v1/comments/{comment_id}`               | Delete a comment (owner/Admin only)                      |

### Engagement Analytics
| Method | Endpoint                                    | Description                                               |
|--------|---------------------------------------------|-----------------------------------------------------------|
| GET    | `/api/v1/analytics/top-users/`               | Get most active users (Admins only)                      |
| GET    | `/api/v1/analytics/top-articles/`            | Get most viewed articles                                  |
| GET    | `/api/v1/analytics/most-commented/`          | Get most commented articles                              |
| GET    | `/api/v1/analytics/user/{user_id}`            | Get engagement stats for a specific user                  |

### Badges & Achievements
| Method | Endpoint                           | Description                                               |
|--------|------------------------------------|-----------------------------------------------------------|
| GET    | `/api/v1/badges/assign/`            | Assign/update badges for the authenticated user           |
| GET    | `/api/v1/badges/user/{user_id}`     | Retrieve badges earned by a user                          |

### Admin Dashboard
| Method | Endpoint                                    | Description                                                |
|--------|---------------------------------------------|------------------------------------------------------------|
| GET    | `/api/v1/admin/moderation-queue/`            | Retrieve pending articles for admin approval                |
| POST   | `/api/v1/admin/approve-article/{article_id}` | Approve an article                                         |
| DELETE | `/api/v1/admin/delete-article/{article_id}`  | Delete an article                                          |
| GET    | `/api/v1/admin/flagged-comments/`            | Get flagged comments for review                            |
| DELETE | `/api/v1/admin/delete-comment/{comment_id}`  | Delete a flagged comment                                   |
| POST   | `/api/v1/admin/ban-user/{user_id}`           | Ban a user                                                 |
| POST   | `/api/v1/admin/restore-user/{user_id}`       | Restore a banned user                                      |
