from flask import Flask
from .routes import auth_bp , main_bp , workspace_bp
from .extensions import loginM , db

# DEFINE CONSTANTS
UPLOAD_FOLDER = "app/static/uploads"
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
 
# Create upload folder if it doesn't exist
 


def create_app():
    # initalise & config 
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "abcd12349e7f82049*/97897'"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
    
    # configure blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(workspace_bp)


    #  configure login manager
    loginM.init_app(app)

    # configure the database
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app      