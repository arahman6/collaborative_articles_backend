import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_DB_URL = os.getenv("MONGODB_URL")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = "HS256"
    # SECTORS = ["Tech", "Health", "Corporate", "Politics", "Youth", "Lifestyle"]
    SECTORS = [
        {
            "sector": "Technology & Innovation",
            "subsectors": [
                "AI Governance", "Quantum Computing", "Bio-Digital Interfaces",
                "Ethical Hacking", "Edge AI", "Neuromorphic Chips",
                "Digital Twin Ecosystems", "Web3 Infrastructure"
            ],
            "audience": "CTOs and tech investors",
            "keywords": ["emerging tech", "digital transformation", "innovation policy"],
            "perspective": "Focus on ethical implications"
        },
        {
            "sector": "Sustainable Development",
            "subsectors": [
                "Circular Cities", "Blue Economy", "Carbon Removal Tech",
                "Climate-Resilient Agriculture", "Just Transition Policies",
                "Green Hydrogen", "Biodiversity Credits"
            ],
            "audience": "Policy makers and ESG professionals",
            "keywords": ["net zero", "sustainable finance", "climate adaptation"],
            "perspective": "Balance economic and ecological needs"
        },
        {
            "sector": "Future of Work",
            "subsectors": [
                "AI Copilots", "Four-Day Workweek", "Skills Obsolescence",
                "Digital Nomad Visas", "Neurodiverse Teams", 
                "Robot Tax Proposals", "Metaverse Workspaces"
            ],
            "audience": "HR leaders and remote workers",
            "keywords": ["workplace evolution", "labor trends", "digital collaboration"],
            "perspective": "Human-centric automation"
        },
        {
            "sector": "Geopolitics",
            "subsectors": [
                "Semiconductor Wars", "Arctic Resource Competition", 
                "Digital Sovereignty", "Climate Migration Treaties",
                "Space Militarization", "Rare Earth Diplomacy"
            ],
            "audience": "Foreign policy analysts",
            "keywords": ["power shifts", "strategic resources", "global governance"],
            "perspective": "Emerging multipolar dynamics"
        },
        {
            "sector": "Health Evolution",
            "subsectors": [
                "Gene Editing Ethics", "AI Drug Discovery", 
                "Microbiome Therapies", "Hospital-at-Home Models",
                "Mental Health Tech", "Longevity Economy"
            ],
            "audience": "Medical professionals and patients",
            "keywords": ["healthtech", "precision medicine", "care innovation"],
            "perspective": "Prevention-over-treatment paradigm"
        },
        {
            "sector": "Consumer Evolution",
            "subsectors": [
                "Deinfluencing Movement", "Anti-Algorithm Shopping",
                "Quiet Luxury", "Digital Ownership",
                "Generational Spending Shifts", "Sensory Commerce"
            ],
            "audience": "Brand strategists and millennials",
            "keywords": ["consumer trends", "retail innovation", "buyer psychology"],
            "perspective": "Post-materialist values"
        },
        {
            "sector": "Urban Futures",
            "subsectors": [
                "15-Minute Cities", "Vertical Farming Systems",
                "Mobility-as-a-Service", "Disaster-Proof Architecture",
                "Smart Slums", "Underground Urbanism"
            ],
            "audience": "Urban planners and residents",
            "keywords": ["smart cities", "urban resilience", "community design"],
            "perspective": "Equitable urbanization"
        }
    ]

config = Config()
