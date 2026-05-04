from flask import render_template , Blueprint  , request, current_app
from flask_login import login_required , current_user
from functools import wraps

import pandas as pd

main_bp = Blueprint("main",__name__)


@main_bp.route("/")
@login_required
def index():
    return render_template("index.html")

@main_bp.route("/workspace")
def workspace():
    # get datasets
    from config import ALLOWED_EXT_DATASET
    from app import UPLOAD_FOLDER
    import os
    print(os.listdir())
    datasets = [i for i in os.listdir(UPLOAD_FOLDER) if i.split(".")[-1] in ALLOWED_EXT_DATASET]
    return render_template("workspace.html",datasets=datasets)


@main_bp.route("/datasets/<dataset>")
def datasetReader(dataset=None):
    if dataset is None :
        return "NO DATASET"
    
    import requests

    data = requests.post("http://127.0.0.1:8080/datasetviewer",data={
        "dataset":dataset
    })
    return render_template("view_dataset.html",dataset=data)

# api
@main_bp.route("/datasetviewer",methods=["POST"])
def viewdata():
    from pandas.errors import EmptyDataError
    from app import UPLOAD_FOLDER

    dataset = request.form.get("dataset")
    ext = dataset.split(".")[-1]
    if ext == "csv":
        try :
            df = pd.read_csv(f"{UPLOAD_FOLDER}/{dataset}")
            df.to_json(f"{UPLOAD_FOLDER}/temp/{dataset.split('.')[:-1]}.json", orient='records')       
        except EmptyDataError as e :
            return "NO COLOMNS (fAILED TO PARSE COLOMNS)"
        jsoned = pd.read_json(f"{UPLOAD_FOLDER}/temp/{dataset}").to_json()
        
        return jsoned
    return "None"