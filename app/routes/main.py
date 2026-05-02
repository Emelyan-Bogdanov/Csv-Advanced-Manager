from flask import render_template , Blueprint ,redirect , url_for , request
from flask_login import login_required , current_user
from functools import wraps

main_bp = Blueprint("main",__name__)




def workspace_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.hasWorkspace():
            return render_template("createworkspace.html",workspace_error="At least create one workspace")
        return f(*args, **kwargs)
    return decorated


@main_bp.route("/")
@login_required
def index():
    return render_template("index.html")

@main_bp.route("/workspace")
# @workspace_required
@login_required
def workspace():
    return render_template("workspace.html")

@main_bp.route("/createworkspace",methods=["POST","GET"])
@login_required
def createworkspace():
    if current_user.hasWorkspace():
        return redirect(url_for("main.workspace"))
    if request.method == "POST" :
        workspacename = request.form.get("workspacename")
        if workspacename.strip() != "":
            current_user.Wok(workspacename)

        else :
            return render_template("createworkspace.html",workspace_error="wokspace name cannot be empty !")

    return render_template("createworkspace.html",workspace_error="at least create one workspace")