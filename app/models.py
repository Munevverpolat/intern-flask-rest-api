from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)

    firstname = db.Column(db.String(80), nullable=False)

    middlename = db.Column(db.String(80))

    lastname = db.Column(db.String(80), nullable=False)

    birthdate = db.Column(db.String(20))

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(256), nullable=False)
    
    salt = db.Column(db.String(64), nullable=False)

class OnlineUser(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        nullable=False
    )

    ipaddress = db.Column(
        db.String(100),
        nullable=False
    )

    logindatetime = db.Column(
        db.DateTime,
        nullable=False
    )