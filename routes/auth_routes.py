from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from flask_bcrypt import Bcrypt
from models.user_model import create_user, find_user_by_email, save_profile_picture
from utils.helpers import validate_email, validate_password
import os
from werkzeug.utils import secure_filename

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        profile_picture = request.files.get('profile_picture')
        
        # Validation
        errors = []
        
        if not name:
            errors.append("Name is required")
        
        if not validate_email(email):
            errors.append("Valid email is required")
        
        if not validate_password(password):
            errors.append("Password must be at least 8 characters long")
        
        # Validate profile picture if provided
        profile_pic_filename = None
        if profile_picture and profile_picture.filename:
            if not allowed_file(profile_picture.filename):
                errors.append("Invalid file type. Please upload PNG, JPG, JPEG, or GIF files only")
            else:
                profile_pic_filename = secure_filename(profile_picture.filename)
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html')
        
        # Check if user already exists
        if find_user_by_email(email):
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        # Hash password and create user
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user_id = create_user(name, email, password_hash, profile_pic_filename)
        
        if user_id:
            # Save profile picture if provided
            if profile_picture and profile_pic_filename:
                save_profile_picture(user_id, profile_picture)
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Registration failed. Please try again.', 'error')
            return render_template('register.html')
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Email and password are required', 'error')
            return render_template('login.html')
        
        user = find_user_by_email(email)
        
        if user and bcrypt.check_password_hash(user['password_hash'], password):
            session['user_id'] = user['_id']
            session['email'] = user['email']
            session['name'] = user['name']
            flash(f'Welcome back, {user["name"]}!', 'success')
            return redirect(url_for('medical.dashboard'))
        else:
            flash('Invalid email or password', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))