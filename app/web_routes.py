from flask import Blueprint, redirect, render_template, url_for


web = Blueprint("web", __name__)


@web.route("/")
def home():
    return redirect(url_for("web.login_page"))


@web.route("/login-page")
def login_page():
    return render_template("login.html")


@web.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@web.route("/users")
def users():
    return render_template("users.html")


@web.route("/users/create")
def create_user_page():
    return render_template("create_user.html")


@web.route("/users/edit/<int:user_id>")
def edit_user_page(user_id):
    return render_template(
        "edit_user.html",
        user_id=user_id,
    )


@web.route("/online-users")
def online_users():
    return render_template("online_users.html")