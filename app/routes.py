import re
from werkzeug.security import generate_password_hash
from flask import Blueprint, jsonify, request
from app import db
from app.models import User

def is_valid_email(email):

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    return re.match(pattern, email)


def is_valid_password(password):

    pattern = \
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'

    return re.match(pattern, password)

main = Blueprint("main", __name__)

@main.route("/health")
def health():
    return jsonify({
        "status": "ok"
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

    user = User(
        username=data["username"],
        firstname=data["firstname"],
        middlename=data.get("middlename"),
        lastname=data["lastname"],
        birthdate=data.get("birthdate"),
        email=data["email"],
        password=generate_password_hash(data["password"])
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User created successfully"
    }), 201
