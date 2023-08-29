from flask import Flask
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv
import os

# Define the Firebase app initialization function
def initialize_firebase_app():
    service_account_key_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")
    cred = credentials.Certificate(service_account_key_path)
    firebase_admin.initialize_app(cred)

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Load environment variables
    load_dotenv()
    
    # Initialize Firebase app
    service_account_key_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")
    cred = credentials.Certificate(service_account_key_path)
    firebase_admin.initialize_app(cred)
    
    # Register Blueprints here
    from .routes import npc_bp
    app.register_blueprint(npc_bp)
    
    return app