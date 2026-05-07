from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
loginM = LoginManager()





@loginM.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))



# redirect to /login endpoint if not logged in
loginM.login_view = "auth.login"
