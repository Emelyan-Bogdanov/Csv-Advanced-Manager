from flask import render_template , Blueprint  , request, current_app
from flask_login import login_required , current_user
from functools import wraps
from .workspace import workspace_required
import pandas as pd

main_bp = Blueprint("main",__name__)


@main_bp.route("/")
@workspace_required
@login_required
def index():
    
    import os

    # get all workspaces of the current user
    from ..models import User
    current_user.createWorkspaceIfNotExists()
    workspaces = None
    try :
        workspaces = os.listdir(current_user.getWorkspacePath())
    except :
        # workspace deleted
        return "WORKSPACE DELETED"
    workspacesData = []
    
    # loop over workspaces
    for workspace in workspaces:
        # loop over datasets
        datasets = []
        for dataset in os.listdir(f"{current_user.getWorkspacePath()}/{workspace}"):
            datasets.append(dataset)
        workspacesData.append(
            {
                "workspace": workspace,
                "datasets":datasets
            }
        )
    
    return render_template("index.html",workspaces=workspacesData)

from .workspace import workspace_required

@login_required
@main_bp.route("/import")
def importF():
    return render_template("workspace/import.html")


@main_bp.route("/raw/<workspace>/<dataset>",methods=["GET"])
def raw(workspace,dataset):
    """return the raw of a file selected"""
    
    # 1. open the file
    filepath = f"{current_user.getWorkspacePath()}{workspace}/{dataset}"
    with open(filepath,"r") as file :
        raws = f"<pre>{file.read()}</pre>"
    return raws