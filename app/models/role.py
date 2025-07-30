from app import db



class Role(db.Model):
    __tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False, unique=True)
    
    def __repr__(self):
        return f"<Role: {self.name}>"