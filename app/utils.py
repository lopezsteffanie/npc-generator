import jwt
from datetime import datetime, timezone, timedelta
from flask import current_app
from . import app

def create_jwt_token(usr_id, user_roles=None):
    # Set the JWt secret key
    secret_key = current_app.config.get("JWT_SECRET_KEY")

    # Define JWT payload with user ID and optional user roles
    payload = {
        "user)id": usr_id,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1) # Set token expiry to 1 day
    }

    if user_roles:
        payload["userRoles"] = user_roles

    return jwt.encode(payload, secret_key, algorithm="HS256")

def validate_jwt_token(token):
    try:
        # Verify the token and get the payload
        payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])

        # Check if the token has expired
        now = datetime.now(timezone.utc)
        return None if now > datetime.fromtimestamp(payload["exp"]) else payload
    except jwt.ExpiredSignatureError:
        return None # Token has expired
    except jwt.InvalidTokenError:
        return None # Token is invalid
    
def create_refresh_token(usr_id):
    # Set the refresh token secret key
    secret_key = current_app.config.get("REFRESH_TOKEN_SECRET_KEY")
    
    payload = {
        "user_id": usr_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=7) # Set refresh token expiry to 7 days
    }
    
    return jwt.encode(payload, secret_key, algorithm="HS256")

def validate_refresh_token(token):
    try:
        # Verify the refresh token and get the user ID
        payload = jwt.decode(token, app.config["REFRESH_TOKEN_SECRET_KEY"], algorithms=["HS256"])
        return payload.get("user_id")
    except jwt.ExpiredSignatureError as e:
        raise jwt.ExpiredSignatureError("Expired refresh token") from e
    except jwt.InvalidTokenError as e:
        raise jwt.InvalidTokenError("Invalid refresh token") from e