from app.tools.csvtools import read_csv_file , read_csv_file_paginated
from app.tools.general import allowed_file
from werkzeug.utils import secure_filename
from flask import Blueprint , render_template , request , jsonify , url_for
from flask import current_app
from config import WORKSPACES_PATH
import os


workspace_bp = Blueprint("workspace",__name__)



# View the dataset
@workspace_bp.route('/view/<filename>')
def view_csv(filename):
    data = read_csv_file(f"{WORKSPACES_PATH}{filename}")
    return render_template('data_view/csv_viewer.html', csv_data=data)

@workspace_bp.route('/view/<filename>/page/<int:page>')
def view_csv_paginated(filename, page):
    data = read_csv_file_paginated(f"{WORKSPACES_PATH}{filename}", page=page)
    return render_template('data_view/csv_viewer.html', csv_data=data)


# afficher la list des datasets & dossiers
@workspace_bp.route("/workspace")
def workspace():
    # get datasets
    from ...config import ALLOWED_EXTENSIONS
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
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Validate file extension
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only CSV files are allowed'}), 400
    
    try:
        # Secure the filename
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Save the file
        file.save(filepath)
        
        # Read and validate CSV
        csv_data = read_csv_file(filepath)
        
        if not csv_data['success']:
            # Delete file if it's invalid
            os.remove(filepath)
            return jsonify({'error': csv_data['error']}), 400
        
        # Return success response
        return jsonify({
            'success': True,
            'filename': filename,
            'total_rows': csv_data['total_rows'],
            'headers': csv_data['headers'],
            'redirect_url': url_for('data_view.csv_viewer', filename=filename)
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500