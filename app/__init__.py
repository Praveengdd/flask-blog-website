from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()


from app.models.user import User
from app.models.role import Role
from app.models.blog import Blog
from app.models.category import BlogCategory
from app.models.comment import Comment
from app.models.like import Likes
from app.models.images import Image

def insert_roles():
    roles = ["admin", "author", "reader"]
    descriptions = ["Standard master", "creates blogs", "reads blogs"]
    
    for i in range(len(roles)):
        if not Role.query.filter_by(name=roles[i]).first():
            db.session.add(Role(name=roles[i], description=descriptions[i]))
        db.session.commit()
        
def insert_blog_categories():
    categories = ["wildlife", "biology", "lifestyle", "finance", "education"]
    
    for category in categories:
        if not BlogCategory.query.filter_by(category=category).first():
            db.session.add(BlogCategory(category=category))
        db.session.commit()

def create_app():
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')
    app.config.from_pyfile('config.py', silent=True)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    csrf.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    with app.app_context():
        insert_roles()
        insert_blog_categories()
    
    from app.blueprints.auth.routes import auth_bp
    from app.blueprints.blog.routes import blog_bp
    from app.blueprints.dashboard.routes import dashboard_bp

    
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(blog_bp, url_prefix="/blog")
    app.register_blueprint(dashboard_bp, url_prefix="/dash")
    
    return app
    
    
    