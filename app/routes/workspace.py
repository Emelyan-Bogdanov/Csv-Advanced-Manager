from app.tools.csvtools import read_csv_file , read_csv_file_paginated
from app.tools.general import allowed_file
from werkzeug.utils import secure_filename
from flask import Blueprint , render_template , request , jsonify , url_for
from flask import current_app


from functools import wraps
from flask import redirect, url_for
from flask_login import current_user


import os

ALLOWED_EXTENSIONS = {'csv'}
WORKSPACES_PATH = "app/static/workspaces/"


# create a decorator in case that the workspace deleted or not found
def workspace_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        # make sure user is authenticated first (important)
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        print("-"*20)
        # check workspace
        if not os.path.exists(current_user.getWorkspacePath()):
            # create workspace
            current_user.createWorkspaceIfNotExists()
            print("=======================USER WORKSPACE RE CREATED")

        return f(*args, **kwargs)

    return wrapper

workspace_bp = Blueprint("workspace",__name__)


# afficher la list des datasets & dossiers
@workspace_bp.route("/workspace")
@workspace_required
def workspace():
    # get datasets
    from app import UPLOAD_FOLDER
    import os
    print(os.listdir())
    datasets = [i for i in os.listdir(UPLOAD_FOLDER) if i.split(".")[-1] in ALLOWED_EXTENSIONS]
    return render_template("workspace/workspace.html",datasets=datasets)


@workspace_bp.route("/newworkspace")
def newworkspace():
    return render_template("workspace/create.html")


# receive a workskspace name through post request , and create its folder
@workspace_bp.route("/createworkspace",methods=["POST"])
def createworkspace():
    # get the workspace name
    workspacename = request.form.get("workspacename")
    
    # check if workspace exists already
    path = f"{current_user.getWorkspacePath()}/{workspacename}"
    if os.path.exists(path) :
        return render_template("workspace/create.html",w_error="workspace already exists")
    
    os.mkdir(path)
    
    return redirect(url_for("main.index"))

@workspace_bp.route("/delete/<path>")
def deleteSubWorkspace(path:str):
    try :
        current_user.deleteWorkspace(path)
    except Exception as e:
        print(f"Can't delete {path} because : {str(e)}")
    return redirect(url_for("main.index",deleted=path)) # delete then return to the home page


# add files & datasets to the workspace
@workspace_bp.route("/addfiles/<filename>",methods=["POST"])
def addfiles():
    return ""




@workspace_bp.route("/add/<workspace>")
def add2workspace(workspace:str):
    # show the import page
    return render_template("workspace/add2workspace.html",workspace=workspace)

@workspace_bp.route("/addFiles",methods=["POST"])
def addFiles():
    workspace = request.form.get("workspace")
    if "fileimported" in request.files :
        file = request.files["fileimported"]
        filename = secure_filename(file.filename)
        path = f"{current_user.getWorkspacePath()}/{workspace}/{filename}"
        file.save(path)
        from colorama import Fore , Style
        print(f"{Fore.GREEN} file saved ")
        return redirect(url_for("main.index"))
    return request.files