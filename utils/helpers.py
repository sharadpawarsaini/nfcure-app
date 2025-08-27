import re
from functools import wraps
from flask import session, redirect, url_for, flash
import qrcode
from PIL import Image

def login_required(f):
    """Decorator to require login for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password (minimum 8 characters)"""
    return len(password) >= 8

def validate_phone(phone):
    """Validate phone number (digits only, 10+ digits)"""
    # Remove spaces, dashes, parentheses
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    # Check if it contains only digits and is at least 10 digits long
    return cleaned.isdigit() and len(cleaned) >= 10

def parse_comma_separated(text):
    """Parse comma-separated text into a list, removing empty items"""
    if not text:
        return []
    items = [item.strip() for item in text.split(',')]
    return [item for item in items if item]  # Remove empty strings

def generate_qr_code(data):
    """Generate QR code from data"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    return img