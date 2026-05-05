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
    workspace_root = db.Column(db.String(50) , nullable=False)
    

    
    def verify_password(self, password):
          return check_password_hash(self.password, password)
    
    def getWorkspacePath(self):
         return f"app/static/workspaces/{self.workspace_root}"

    def createWorkspaceIfNotExists(self):
         import os
         if os.path.exists(self.getWorkspacePath()) :
              return
         else :
              os.mkdir(self.getWorkspacePath())
              print("WORKSPACE CREATED")
              return
              

    # this simulate User.toString()
    def __repr__(self):
        return '<User %r>' % self.username