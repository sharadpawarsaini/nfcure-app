from flask import Flask
from flask import Flask, redirect, url_for
from config import mongo_client, db
from routes.auth_routes import auth_bp
from routes.medical_routes import medical_bp
from routes.main_routes import main_bp
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'e1d92c2d4f3a8b7c1a3d9f7e0c54af9d12a34567a9b0cdfe')

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(medical_bp)

# Ensure unique index on users.email
try:
    db.users.create_index("email", unique=True)
    print("✓ Database index created successfully")
except Exception as e:
    print(f"Database index creation: {e}")

@app.route('/')
def index():
    return redirect(url_for('main.home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
