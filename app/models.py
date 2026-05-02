from .extensions import db , loginM
from flask_login import UserMixin , login_manager
from werkzeug.security import check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model,UserMixin):
    __table_name__ = "users"
    id = db.Column(db.Integer, db.Sequence('id', start=1, increment=1), primary_key=True)
    email = db.Column(db.String(30) , nullable=False , unique=True)
    username = db.Column(db.String(30) , nullable=False)
    password = db.Column(db.String(200) , nullable=False)
    workspace = db.Column(db.String(50) , nullable=False)
    

    
    def verify_password(self, password):
          return check_password_hash(self.password, password)
    
    # this simulate User.toString()
    def __repr__(self):
        return '<User %r>' % self.username