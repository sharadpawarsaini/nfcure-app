import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI')
if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable is required")

try:
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client["nfcure_db"]
    # Test the connection
    mongo_client.admin.command('ping')
    print("✓ Connected to MongoDB Atlas successfully")
except Exception as e:
    print(f"✗ MongoDB connection failed: {e}")
    raise