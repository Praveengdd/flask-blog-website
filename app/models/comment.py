from app import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comment'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False, index=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id', ondelete="CASCADE"), nullable=False, index=True)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    #ORM Relationships
    user = db.relationship('User', backref=db.backref('comments', lazy="dynamic"))
    blog = db.relationship('Blog', backref=db.backref('comments', lazy="dynamic", order_by="Comment.created_at.desc()"))
    
    
    def __repr__(self):
        return f"<Comment: {self.id}>"