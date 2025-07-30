from app import db

class Likes(db.Model):
    __tablename__ = "likes"
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id', ondelete="CASCADE"), primary_key=True)
    
    
    #ORM Relationships
    
    blog = db.relationship('Blog', backref=db.backref('likes', lazy="dynamic"))
    user = db.relationship('User', backref=db.backref('liked_blogs', lazy="dynamic"))
    
    
    def __repr__(self):
        return f"<Like: Blog {self.blog_id} by User {self.user_id}>"