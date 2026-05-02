from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
loginM = LoginManager()





@loginM.user_loader
# THIS IS IMPORTANT
def load_user(email):
    from .models import User
    return User.query.filter_by(email=email).first()


# redirect to /login endpoint if not logged in
loginM.login_view = "auth.login"