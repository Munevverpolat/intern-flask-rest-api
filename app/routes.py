from flask import Blueprint, jsonify, request

from app.models import User
from app import db

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

import re


main = Blueprint("main", __name__)


def is_valid_email(email):

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    return re.match(pattern, email)


def is_valid_password(password):

    pattern = \
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'

    return re.match(pattern, password)


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

    if not check_password_hash(
        user.password,
        data["password"]
    ):

        return jsonify({
            "error": "Wrong password"
        }), 401

    return jsonify({
        "message": "Login successful"
    }), 200