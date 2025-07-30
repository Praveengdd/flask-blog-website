from app import db

class BlogCategory(db.Model):
    __tablename__ = "blog_category"
    
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), unique=True, nullable=False)
    
    
    def __repr__(self):
        return f"<Category: {self.category}>"