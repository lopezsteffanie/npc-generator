from flask import Flask
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv
import os
from .config import JWT_SECRET_KEY

# Define the Firebase app initialization function
def initialize_firebase_app():
    service_account_key_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

<<<<<<< HEAD
# Initialize Firestore client
db = firestore.client()

=======
>>>>>>> db777c3 (Added routes)
def create_app(test_config=None):
    app = Flask(__name__)
    
    # Load environment variables
    load_dotenv()
    
<<<<<<< HEAD
    # Set the JWT_SECRET_KEY in the app's configuration
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    
    # Initialize Firebase app
    initialize_firebase_app()
    
    # TODO: Import models here
    
    # Register Blueprints here
    from .auth_routes import auth_bp
    app.register_blueprint(auth_bp)
=======
    # Initialize Firebase app
    service_account_key_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")
    cred = credentials.Certificate(service_account_key_path)
    firebase_admin.initialize_app(cred)
    
    # Register Blueprints here
    from .routes import npc_bp
    app.register_blueprint(npc_bp)
>>>>>>> db777c3 (Added routes)
    
    return app