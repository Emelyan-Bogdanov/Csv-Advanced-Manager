from flask import render_template , Blueprint  , request, current_app
from flask_login import login_required , current_user
from functools import wraps

import pandas as pd

main_bp = Blueprint("main",__name__)


@main_bp.route("/")
# @login_required
def index():
    return render_template("index.html")


@main_bp.route("/import")
def importF():
    return render_template("workspace/import.html")

