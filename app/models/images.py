from app import db
from datetime import datetime

class Image(db.Model):
    __tablename__ = "image"
    
    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id', ondelete="CASCADE"), nullable=False)
    image_path = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    #ORM Relationships
    blog = db.relationship('Blog', backref=db.backref('images', lazy="dynamic", cascade="all, delete-orphan"))
    
    def __repr__(self):
        return f"Image {self.id} for Blog {self.blog_id}"
    
