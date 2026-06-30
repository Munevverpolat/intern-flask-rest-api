from werkzeug.security import generate_password_hash
from flask import Blueprint, jsonify, request
from app import db
from app.models import User

main = Blueprint("main", __name__)

@main.route("/health")
def health():
    return jsonify({
        "status": "ok"
    })

@main.route("/user/create", methods=["POST"])
def create_user():

    data = request.get_json()

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
