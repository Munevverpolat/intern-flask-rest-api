from flask import (
    Blueprint,
    jsonify,
    request,
    current_app,
    g
)

from datetime import datetime, timedelta

from app import db
from app.models import User, OnlineUser

import re
import jwt
import hashlib
import secrets

from functools import wraps

main = Blueprint("main", __name__)


def is_valid_email(email):

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    return re.match(pattern, email)


def is_valid_password(password):

    pattern = \
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'

    return re.match(pattern, password)

def hash_password(password, salt=None):

    if not salt:
        salt = os.urandom(16).hex()

    hashed = hashlib.sha256(
        (password + salt).encode()
    ).hexdigest()

    return hashed, salt

def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get("Authorization")

        if not token:

            return jsonify({
                "error": "Token missing"
            }), 401

        try:

            token = token.split(" ")[1]

            data = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )

            g.user = data

        except:

            return jsonify({
                "error": "Invalid token"
            }), 401

        return f(*args, **kwargs)

    return decorated

@main.route("/health")
def health():

    return jsonify({
        "message": "API is running"
    })


@main.route("/user/create", methods=["POST"])
def create_user():

    data = request.get_json()

    required_fields = [
        "username",
        "firstname",
        "lastname",
        "email",
        "password"
    ]

    for field in required_fields:

        if field not in data:

            return jsonify({
                "error": f"{field} is required"
            }), 400

    if not is_valid_email(data["email"]):

        return jsonify({
            "error": "Invalid email"
        }), 400

    if not is_valid_password(data["password"]):

        return jsonify({
            "error":
            "Password must contain uppercase, lowercase, number and minimum 8 chars"
        }), 400

    existing_user = User.query.filter_by(
        email=data["email"]
    ).first()

    if existing_user:

        return jsonify({
            "error": "Email already exists"
        }), 409

    salt = secrets.token_hex(16)

    hashed_password = hashlib.sha256(
        (data["password"] + salt).encode()
    ).hexdigest()

    user = User(
        username=data["username"],
        firstname=data["firstname"],
        middlename=data.get("middlename"),
        lastname=data["lastname"],
        birthdate=data.get("birthdate"),
        email=data["email"],
        password=hashed_password,
        salt=salt
    )

    db.session.add(user)
    db.session.commit()

    current_app.logger.info( 
        f"New user registered: {user.username}" 
    )

    return jsonify({
        "message": "User created successfully"
    }), 201
@main.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    required_fields = [
        "email",
        "password"
    ]

    for field in required_fields:

        if field not in data:

            return jsonify({
                "error": f"{field} is required"
            }), 400

    user = User.query.filter_by(
        email=data["email"]
    ).first()

    if not user:

        return jsonify({
            "error": "User not found"
        }), 404

    hashed_input_password = hashlib.sha256(
        (data["password"] + user.salt).encode()
    ).hexdigest()

    if hashed_input_password != user.password:

        return jsonify({
            "error": "Wrong password"
        }), 401

    token = jwt.encode(
        {
            "user_id": user.id,
            "email": user.email,
            "exp": datetime.utcnow() +
            timedelta(hours=1)
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )
    online_user = OnlineUser(
        username=user.username,
        ipaddress=request.remote_addr,
        logindatetime=datetime.utcnow()
    ) 

    db.session.add(online_user)

    db.session.commit()
        
    current_app.logger.info(
    f"User logged in: {user.username}"
    )

    return jsonify({
        "message": "Login successful",
        "token": token
    }), 200

@main.route("/profile", methods=["GET"])
@token_required
def profile():

    user = User.query.get(
        g.user["user_id"]
    )

    return jsonify({
        "id": user.id,
        "username": user.username,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "email": user.email
    }), 200

@main.route("/user/list", methods=["GET"])
@token_required
def user_list():

    users = User.query.all()

    return jsonify([
    {
        "id": user.id,
        "username": user.username,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "email": user.email
    }
    for user in users
]), 200

@main.route("/user/update/<int:id>", methods=["PUT"])
@token_required
def update_user(id):

    data = request.get_json()

    user = User.query.get(id)

    if not user:

        return jsonify({
            "error": "User not found"
        }), 404

    user.firstname = data.get(
        "firstname",
        user.firstname
    )

    user.lastname = data.get(
        "lastname",
        user.lastname
    )

    user.email = data.get(
        "email",
        user.email
    )

    db.session.commit()

    return jsonify({
        "message": "User updated successfully"
    }), 200

@main.route("/user/delete/<int:id>", methods=["DELETE"])
@token_required
def delete_user(id):

    user = User.query.get(id)

    if not user:

        return jsonify({
            "error": "User not found"
        }), 404

    db.session.delete(user)

    db.session.commit()

    current_app.logger.info( 
        f"User deleted: {user.username}" 
    )

    return jsonify({
        "message": "User deleted successfully"
    }), 200

@main.route("/logout", methods=["POST"])
@token_required
def logout():

    current_app.logger.info(
         f"User logged out: {g.user['email']}" 
    )

    return jsonify({
        "message": "Logout successful"
    }), 200

@main.route("/onlineusers", methods=["GET"])
@token_required
def online_users():

    online_users = OnlineUser.query.all()

    result = []

    for user in online_users:

        result.append({
            "id": user.id,
            "username": user.username,
            "ipaddress": user.ipaddress,
            "logindatetime": user.logindatetime
        })

    return jsonify(result), 200