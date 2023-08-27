from flask import Flask, request, jsonify, Blueprint
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import os



def create_app(test_config=None):
    app = Flask(__name__)
    
    # Load environment variables
    load_dotenv()
    
    # Initialize Firebase app
    service_account_key_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    
    # Import models here
    # db = firestore client()
    
    # Register Blueprints here
    from .routes import hello_world_bp
    app.register_blueprint(hello_world_bp)
    
    return app