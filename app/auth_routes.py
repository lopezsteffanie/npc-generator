from flask import Blueprint, request, redirect, url_for, make_response, jsonify, flash
from firebase_admin import auth
from .auth import login_required, email_verified_required
from app import db, initialize_firebase_app
from .utils import create_jwt_token, validate_jwt_token, create_refresh_token, validate_refresh_token
from datetime import datetime, timedelta, timezone
from . import auth_bp
from . import app

initialize_firebase_app()

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    email = request.form['email']
    password = request.form['password']
    display_name = request.form['displayName']
    user_preferences = {"theme": "default" } # Default user preferences
    user_roles = ["user"] # Default user role]
    
    try:
        user = auth.create_user(email=email, password=password)
        
        # Store additional user data in Firestore
        firestore_user_data = {
            "email": user.email,
            "uid": user.uid,
            "displayName": display_name,
            "userPreferences": user_preferences,
            "userRoles": user_roles
            # TODO: Add more fields as needed
        }
        db.collection("users").document(user.uid).set(firestore_user_data)
        
        # Generate and send email verification link
        verification_link = auth.generate_email_verification_link(user.email)
        
        return jsonify({"message": "Registration successful"}), 201
    except auth.AuthError as e:
        error_message = e.detail.get("message") if e.detail else "Registration failed"
        return jsonify({"error": error_message}), 400
    
@auth_bp.route("/login", methods=["POST"])
@email_verified_required
def login():
    email = request.form['email']
    password = request.form['password']

    try:
        user = auth.sign_in_with_email_and_password(email=email, password=password)

        # Retrieve user roles from Firestore and include them in the JWT claims
        user_roles = db.collection("users").document(user.uid).get().get("userRoles", [])
        jwt_token_with_claims = create_jwt_token(user.uid, user_roles=user_roles)

        # Generate JWT tokens (access and refresh tokens)
        jwt_token = create_jwt_token(user.uid)
        refresh_token = create_refresh_token(user.uid)

        # Set access token as a cookie with secure and HttpOnly flags, and a shorter expiration time
        expiration_time = datetime.now(timezone.utc) + timedelta(minutes=30)
        response = make_response(jsonify({"message": "Login successful"}), 200)
        response.set_cookie("jwt_token", jwt_token, secure=True, httponly=True, expires=expiration_time)

        # Set refresh token as a cookie with secure and HttpOnly flags, and a longer expiration time
        refresh_expiration_time = datetime.now(timezone.utc) + timedelta(days=7)  # Set refresh token expiry to 7 days
        response.set_cookie("refresh_token", refresh_token, secure=True, httponly=True, expires=refresh_expiration_time)

        return response
    except auth.AuthError as e:
        error_message = e.detail.get("message") if e.detail else "Login failed"
        return jsonify({"error": error_message}), 401

@auth_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    # Retrieve token from cookie
    jwt_token = request.cookies.get("jwt_token")

    # Validate the token
    if jwt_token:
        token_payload = validate_jwt_token(jwt_token)
        if token_payload is None:
            # Invalid or expired token
            flash("Invalid or expired token. Please log in again.", "error")
            return redirect(url_for("auth.login"))
    
    # Clear the user's session and token
    response = make_response(redirect(url_for('auth.login')))
    response.delete_cookie('jwt_token')  # Remove the token cookie
        
    # Log the logout event
    user_id = token_payload.get("user_id") if token_payload else "unknown"
    app.logger.info(f"User logged out. User ID: {user_id}")
        
    # Notify the user
    flash("You have been successfully logged out.", "success")
    
    return response

@auth_bp.route("/refresh", methods=["POST"])
def refresh_token():
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        try:
            user_id = validate_refresh_token(refresh_token)  # Implement this function
            new_access_token = create_jwt_token(user_id)
            response = make_response(jsonify({"access_token": new_access_token}), 200)
            return response
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Expired refresh token"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid refresh token"}), 401
    else:
        return jsonify({"error": "Missing refresh token"}), 401

@auth_bp.route("/protected", methods=["GET"])
@login_required
def protected_route():
    if token := request.cookies.get('jwt_token'):
        return (
            jsonify({"message": "Access granted"})
            if (token_payload := validate_jwt_token(token))
            else (jsonify({"error": "Invalid or expired token"}), 401)
        )
    else:
        return jsonify({"error": "Missing token"}), 401