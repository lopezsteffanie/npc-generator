from flask import Flask
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv
import os
import json
from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Load environment variables
    # load_dotenv()
    
    # Initialize Firebase app
    service_account_key_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")
    cred = credentials.Certificate(json.loads(service_account_key_json))
    firebase_admin.initialize_app(cred)
    
    # # Allow requests from the React development server
    # CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    # Enable CORS for all routes
    CORS(app)
    
    # Register Blueprints here
    from .routes import npc_bp
    app.register_blueprint(npc_bp)
    
    return app