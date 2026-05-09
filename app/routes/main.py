from flask import render_template , Blueprint  , request, current_app
from flask_login import login_required , current_user
from functools import wraps
from .workspace import workspace_required
import pandas as pd
from flask import Response
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
        raws = f"{file.read()}"
    return Response(raws,mimetype="text/plain") if ".html" in filepath else f"<pre>{raws}</pre>"





"""
Add this function to app/routes/main.py
"""

@main_bp.route("/view/<workspace>/<dataset>", methods=["GET"])
@login_required
def view_csv(workspace,dataset):
    """
    View a CSV file in the browser.
    
    Args:
        filename: The CSV filename with path (e.g., workspace/dataset.csv)
    
    Returns:
        Rendered HTML template with CSV data
    """
    import os
    import pandas as pd
    from werkzeug.utils import secure_filename
    
    try:
        # Sanitize and validate filename to prevent directory traversal
        # Filename should contain workspace/filename.csv format
        
        
        # Construct full file path
        filepath = os.path.join(current_user.getWorkspacePath(), workspace, dataset)
        
        # Verify file exists
        if not os.path.exists(filepath):
            return render_template("data_view/csv_view.html", 
                                 error=True, 
                                 error_message="File not found"), 404
        
        # Verify file is within user's workspace (security check)
        real_path = os.path.realpath(filepath)
        workspace_path = os.path.realpath(current_user.getWorkspacePath())
        
        if not real_path.startswith(workspace_path):
            return render_template("data_view/csv_view.html", 
                                 error=True, 
                                 error_message="Unauthorized access"), 403
        
        # Verify file is a CSV
        if not filepath.lower().endswith('.csv'):
            return render_template("data_view/csv_view.html", 
                                 error=True, 
                                 error_message="Only CSV files are supported"), 400
        
        # Load CSV file with pandas
        try:
            df = pd.read_csv(filepath)
        except pd.errors.EmptyDataError:
            return render_template("data_view/csv_view.html", 
                                 error=True, 
                                 error_message="CSV file is empty"), 400
        except Exception as e:
            return render_template("data_view/csv_view.html", 
                                 error=True, 
                                 error_message=f"Error reading CSV: {str(e)}"), 400
        
        # Prepare data for template
        csv_data = {
            'filename': dataset,
            'success': True,
            'error': None,
            'headers': df.columns.tolist(),
            'rows': df.to_dict('records'),
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'data_types': df.dtypes.to_dict(),
            'preview_rows': 50  # Show first 50 rows
        }
        
        return render_template("data_view/view.html", csv_data=csv_data)
    
    except Exception as e:
        return render_template("data_view/view.html", 
                             error=True, 
                             error_message=f"Unexpected error: {str(e)}"), 500