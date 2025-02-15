# Collaborative Articles API

**Collaborative Articles API** is a serverless FastAPI backend that allows users to contribute to AI-generated articles on various topics like **Tech, Health, Corporate, Politics, Youth, and Lifestyle**. The API is deployed using **AWS Lambda + API Gateway** via AWS SAM.

## 📂 Project Structure
```
fastapi-sam/
│── app/
│   ├── main.py                # FastAPI entry point
│   ├── config.py              # Configuration settings
│   ├── database.py            # MongoDB connection
│   ├── models/                # Pydantic models
│   ├── routers/               # API routes (articles, users, comments, contributions)
│   ├── services/              # Business logic (OpenAI, authentication)
│── tests/                     # Unit & integration tests
│── handler.py                  # AWS Lambda entry point
│── requirements.txt            # Python dependencies
│── template.yml                # AWS SAM configuration
│── .gitignore                  # Ignore unnecessary files
│── README.md                   # Documentation
```

## 🛠 Installation & Setup
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

## 🏗️ Running Locally
Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
Access the API documentation at:
- **Swagger UI** → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc** → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🧪 Running Tests
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

## 🔑 Authentication & JWT
- Users can **signup & login** using JWT authentication.
- JWT secret is stored in **AWS SSM Parameter Store** for security.

## 📌 API Endpoints
### **🔹 Articles**
| Method | Endpoint                 | Description                  |
|--------|--------------------------|------------------------------|
| `POST` | `/api/v1/articles/`       | Create a new article        |
| `GET`  | `/api/v1/articles/`       | Get all articles            |
| `GET`  | `/api/v1/articles/{id}`   | Get an article by ID        |
| `PUT`  | `/api/v1/articles/{id}`   | Update an article           |
| `DELETE` | `/api/v1/articles/{id}` | Delete an article           |

### **🔹 Users**
| Method | Endpoint                 | Description                  |
|--------|--------------------------|------------------------------|
| `POST` | `/api/v1/signup/`        | Register a new user         |
| `POST` | `/api/v1/login/`         | User login & JWT generation |

### **🔹 Contributions & Comments**
| Method | Endpoint                    | Description                     |
|--------|-----------------------------|---------------------------------|
| `POST` | `/api/v1/contributions/`     | Add a contribution to an article |
| `GET`  | `/api/v1/contributions/`     | Get all contributions           |
| `POST` | `/api/v1/comments/`          | Add a comment to an article     |
| `GET`  | `/api/v1/comments/`          | Get all comments                |
