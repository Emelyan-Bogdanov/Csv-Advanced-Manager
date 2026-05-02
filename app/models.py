from .extensions import db , loginM
from flask_login import UserMixin , login_manager
from werkzeug.security import check_password_hash

class User(db.Model,UserMixin):
    __table_name__ = "users"
    id = db.Column(db.Integer, db.Sequence('id', start=1, increment=1), primary_key=True)
    email = db.Column(db.String(30) , nullable=False , unique=True)
    username = db.Column(db.String(30) , nullable=False)
    password = db.Column(db.String(200) , nullable=False)
    workspace = db.Column(db.String(50) , nullable=True , default="[noworkspace]")
    

    def hasWorkspace(self):
         return self.workspace != "[noworkspace]"
    
    # set a workspace
    def setWorkspace(self,workspaceName:str):
         self.workspace = workspaceName

#    def is_active(self):
#          return self.active
    
    def verify_password(self, password):
          return check_password_hash(self.password, password)
