from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db
from werkzeug.security import check_password_hash, generate_password_hash



roles_users = db.Table("roles_users",
                       db.Column("user_id", db.Integer(), db.ForeignKey('user.id', ondelete="CASCADE")),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id', ondelete="CASCADE"))
)




class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False, index=True)
    password = db.Column(db.String(250), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)
    
    #Relationships
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))
    
    def set_password(self, password):
        self.password = generate_password_hash(password, method="scrypt:32768:8:1")
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f"<User {self.email}>"