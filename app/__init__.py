from flask import Flask
from .routes import auth_bp , main_bp , visualise_bp , manage_bp
from .extensions import loginM , db

# DEFINE CONSTANTS
UPLOAD_FOLDER = "app/static/uploads"

def create_app():
    # initalise & config 
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "abcd12349e7f97897'"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    # configure blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(manage_bp)
    app.register_blueprint(visualise_bp)

    

    # configure logger

    #  configure login manager
    loginM.init_app(app)

    # configure the database
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app      