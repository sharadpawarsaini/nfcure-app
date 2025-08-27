from config import db
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
import os
from werkzeug.utils import secure_filename

def create_user(name, email, password_hash, profile_picture=None):
    """Create a new user in the database"""
    try:
        user_data = {
            "name": name,
            "email": email,
            "password_hash": password_hash,
            "profile_picture": profile_picture
        }
        result = db.users.insert_one(user_data)
        return str(result.inserted_id)
    except DuplicateKeyError:
        return None

def save_profile_picture(user_id, file):
    """Save profile picture to static/uploads directory"""
    try:
        # Create uploads directory if it doesn't exist
        upload_dir = os.path.join('static', 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        filename = f"{user_id}_{secure_filename(file.filename)}"
        filepath = os.path.join(upload_dir, filename)
        
        # Save file
        file.save(filepath)
        
        # Update user record with filename
        db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"profile_picture": filename}}
        )
        
        return filename
    except Exception as e:
        print(f"Error saving profile picture: {e}")
        return None

def find_user_by_email(email):
    """Find a user by email"""
    user = db.users.find_one({"email": email})
    if user:
        user["_id"] = str(user["_id"])
    return user

def find_user_by_id(user_id):
    """Find a user by ID"""
    try:
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            user["_id"] = str(user["_id"])
        return user
    except Exception:
        return None

def get_profile(user_id):
    """Get user's medical profile"""
    try:
        profile = db.profiles.find_one({"user_id": user_id})
        if profile:
            profile["_id"] = str(profile["_id"])
        return profile
    except Exception:
        return None

def upsert_profile(user_id, profile_dict):
    """Create or update user's medical profile"""
    try:
        profile_data = {
            "user_id": user_id,
            **profile_dict
        }
        result = db.profiles.update_one(
            {"user_id": user_id},
            {"$set": profile_data},
            upsert=True
        )
        return result.acknowledged
    except Exception:
        return False