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
         self.createWorkspaceIfNotExists()
         return f"app/static/workspaces/{self.workspace_root}"

    def createWorkspaceIfNotExists(self):
         import os
         if os.path.exists(f"app/static/workspaces/{self.workspace_root}") :
              return
         else :
              os.mkdir(f"app/static/workspaces/{self.workspace_root}")
              print("WORKSPACE CREATED")
              return
     
     # delete sub workspace
    def deleteWorkspace(self,path:str):
         root = self.getWorkspacePath()
         # if exits => delete
         from colorama import Fore , Style
         import os
         import os
         import stat
         import shutil

         def remove_readonly(func, path, _):
              os.chmod(path, stat.S_IWRITE)
              func(path)
              shutil.rmtree(
                   f"{root}/{path}",
                   onerror=remove_readonly
              )
         print("===========>",f"{root}/{path}")
         if os.path.exists(f"{root}/{path}") :
               os.remove(f"{root}/{path}")
               print(f"{Fore.RED}workspace deleted : {path}{Style.RESET_ALL}")
          
    # this simulate User.toString()
    def __repr__(self):
        return '<User %r>' % self.username