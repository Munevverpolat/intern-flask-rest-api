# Intern Flask REST API

This project is developed as part of internship tasks using Flask and PostgreSQL.

## Features

* RESTful API
* PostgreSQL database
* SQLAlchemy ORM
* JWT Authentication
* Password hashing with SHA256 + salt
* Email and password validation
* Logging system
* Flask-Migrate support
* Environment variable management with `.env`

## Endpoints

* `/login`
* `/logout`
* `/user/create`
* `/user/list`
* `/user/update/<id>`
* `/user/delete/<id>`
* `/onlineusers`
* `/health`

## Technologies

* Flask
* PostgreSQL
* SQLAlchemy
* Flask-Migrate
* PyJWT
* Python Dotenv

## Installation

git clone <repository_url>
cd intern-flask-rest-api

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

## Environment Variables

Create a `.env` file:

SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://postgres:password@localhost/intern_flask_db

## Run Application

python run.py