from app import db
from datetime import datetime

class Blog(db.Model):
    __tablename__='blog'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('blog_category.id', ondelete="CASCADE"), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(150), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    #ORM Relationships
    user = db.relationship('User', backref=db.backref('blogs', lazy="dynamic"))
    category = db.relationship('BlogCategory', backref=db.backref('blogs', lazy="dynamic"))
    
    
    
    def __repr__(self):
        return f"<blog {self.id}>"
    