from flask import Blueprint , render_template , request , redirect , current_app
from flask_login import login_user , current_user
from flask import url_for
from ..models import User
from ..extensions import db
from werkzeug.security import generate_password_hash

auth_bp = Blueprint("auth",__name__)

@auth_bp.route("/login" , methods=["POST","GET"])
def login():
    if request.method == "POST":
        Email = request.form.get("email")
        password = request.form.get("password")

        # check if user exists
        user = User.query.filter_by(email=Email).first()
        if user is None :
            return render_template("/auth/login.html",e_error="user not found")
        else :
            if user.verify_password(password) :
                login_user(user)
                return redirect(url_for("main.index"))
            else :
                return render_template("/auth/login.html",p_error="password wrong")
    return render_template("/auth/login.html")


@auth_bp.route("/register",methods=["POST","GET"])
def register():
    if request.method == "POST" :
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        workspacename = request.form.get("workspacename")

        user = User.query.filter_by(email=email).first()
        if user is  None :
            new_user = User(
                email=email,
                username=username,
                password=generate_password_hash(password),
                workspace_root=workspacename 
                )
            new_user.createWorkspaceIfNotExists()
            db.session.add(new_user)
            db.session.commit()
            
            login_user(new_user) # if you want to log in from sign up then redirect directly to home page
            # save action to log
            # current_app.logger.info(f"[USER] new user created email={new_user.email}")
            current_user.createWorkspaceIfNotExists()
            return redirect(url_for("auth.login"))
        else :
            return render_template("auth/register.html",e_error="User with that email Already exists")

    return render_template("/auth/register.html")

@auth_bp.route("/logout")
def logout():
    from flask_login import logout_user
    logout_user()
    return redirect(url_for("auth.login"))