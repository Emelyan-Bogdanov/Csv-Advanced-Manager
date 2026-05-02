from flask import Blueprint , render_template , request , redirect , url_for
from flask_login import login_required , logout_user , login_user , current_user
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
            return render_template("login.html",e_error="user not found")
        else :
            if user.verify_password(password) :
                login_user(user)
                print("="*50)
                return redirect("/workspace")
            else :
                return render_template("login.html",p_error="password wrong")
    return render_template("login.html")


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
                workspace=workspacename 
                )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user) #
            current_user.createWorkspaceIfNotExists()
            return redirect("/workspace")
        else :
            return render_template("register.html",e_error="User with that email Already exists")

    return render_template("register.html")