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



# View the dataset
@workspace_required
@workspace_bp.route('/view/<filename>')
def view_csv(filename):
    data = read_csv_file(f"{WORKSPACES_PATH}{filename}")
    return render_template('data_view/csv_viewer.html', csv_data=data)

@workspace_required
@workspace_bp.route('/view/<filename>/page/<int:page>')
def view_csv_paginated(filename, page):
    data = read_csv_file_paginated(f"{WORKSPACES_PATH}{filename}", page=page)
    return render_template('data_view/csv_viewer.html', csv_data=data)


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



@workspace_bp.route('/upload', methods=['POST'])
def upload_file():
    """Handle CSV file upload"""
    
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']

    print(file.filename,"====="*50)
    return ""


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
    
    return render_template("index.html")

@workspace_bp.route("/delete/<path>")
def deleteSubWorkspace(path:str):
    try :
        current_user.deleteWorkspace(path)
    except Exception as e:
        print(f"Can't delete {path} because : {str(e)}")
    return redirect(url_for("main.index",deleted=path)) # delete then return to the home page