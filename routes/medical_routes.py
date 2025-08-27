from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file
from models.user_model import get_profile, upsert_profile
from utils.helpers import login_required, validate_phone, parse_comma_separated, generate_qr_code
import json
import io
import base64

medical_bp = Blueprint('medical', __name__)

@medical_bp.route('/dashboard')
@login_required
def dashboard():
    user_id = session.get('user_id')
    profile = get_profile(user_id)
    
    return render_template('dashboard.html', profile=profile)

@medical_bp.route('/profile', methods=['POST'])
@login_required
def update_profile():
    user_id = session.get('user_id')
    
    # Get form data
    blood_group = request.form.get('blood_group', '').strip()
    allergies_raw = request.form.get('allergies', '').strip()
    emergency_name = request.form.get('emergency_name', '').strip()
    emergency_phone = request.form.get('emergency_phone', '').strip()
    medical_conditions_raw = request.form.get('medical_conditions', '').strip()
    
    # Validation
    errors = []
    
    if not blood_group:
        errors.append("Blood group is required")
    
    if not emergency_name:
        errors.append("Emergency contact name is required")
    
    if not validate_phone(emergency_phone):
        errors.append("Valid emergency contact phone is required")
    
    if errors:
        for error in errors:
            flash(error, 'error')
        return redirect(url_for('medical.dashboard'))
    
    # Parse comma-separated lists
    allergies = parse_comma_separated(allergies_raw)
    medical_conditions = parse_comma_separated(medical_conditions_raw)
    
    # Prepare profile data
    profile_data = {
        'blood_group': blood_group,
        'allergies': allergies,
        'emergency_contact': {
            'name': emergency_name,
            'phone': emergency_phone
        },
        'medical_conditions': medical_conditions
    }
    
    # Save profile
    if upsert_profile(user_id, profile_data):
        flash('Medical profile updated successfully!', 'success')
    else:
        flash('Failed to update profile. Please try again.', 'error')
    
    return redirect(url_for('medical.dashboard'))

@medical_bp.route('/qr-code')
@login_required
def generate_qr():
    user_id = session.get('user_id')
    profile = get_profile(user_id)
    
    if not profile:
        flash('Please create your medical profile first', 'error')
        return redirect(url_for('medical.dashboard'))
    
    # Prepare medical data for QR code
    medical_data = {
        'name': session.get('name'),
        'blood_group': profile.get('blood_group'),
        'allergies': profile.get('allergies', []),
        'emergency_contact': profile.get('emergency_contact', {}),
        'medical_conditions': profile.get('medical_conditions', [])
    }
    
    # Generate QR code
    qr_img = generate_qr_code(json.dumps(medical_data))
    
    # Convert to base64 for display
    img_buffer = io.BytesIO()
    qr_img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    qr_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    
    return render_template('qr_code.html', qr_code=qr_base64, medical_data=medical_data)