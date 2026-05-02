from flask import render_template , Blueprint ,redirect , url_for , request
from flask_login import login_required , current_user
from functools import wraps

main_bp = Blueprint("main",__name__)






@main_bp.route("/")
@login_required
def index():
    return render_template("index.html")

@main_bp.route("/workspace")
@login_required
def workspace():
    return render_template("workspace.html")