import os
from flask import Blueprint, render_template, request, url_for, redirect, abort, flash, get_flashed_messages
from werkzeug.utils import secure_filename
from app.utils.decorators import roles_required
from flask_login import login_required, current_user
from app.models.user import User
from app.models.blog import Blog
from app.models.comment import Comment
from app.models.category import BlogCategory
from app.models.like import Likes
from app.models.images import Image
from app import db

blog_bp = Blueprint("blog", __name__)



@blog_bp.route("/all_blogs")
@roles_required("admin", "author", "reader")
@login_required
def all_blogs():
    all_blogs = Blog.query.all()
    return render_template("blog/all_blogs.html", all_blogs=all_blogs)



@blog_bp.route("/view_blog/<int:blog_id>", methods=["GET", "POST"])
@roles_required("admin", "author", "reader")
@login_required
def view_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    comments = blog.comments
    liked = Likes.query.filter_by(user_id=current_user.id, blog_id=blog.id).first()
    images = blog.images

    if request.method == "POST":
        comment_text = request.form.get("comment", "").strip()
    
        if comment_text:
            comment = Comment(user_id=current_user.id,
                                  blog_id=blog.id,
                                  comment=comment_text)
            db.session.add(comment)
            db.session.commit()
                
            return redirect(url_for("blog.view_blog", blog_id=blog.id))
                
        else:
            flash("Entered comment is empty", "warning")
            return redirect(url_for("blog.view_blog", blog_id=blog.id))
                
                
    return render_template("blog/view_blog.html", blog=blog, comments=comments, user=current_user, liked=liked, images=images)



@blog_bp.route("/toggle_like/<int:blog_id>", methods=["POST"])
@roles_required("admin", "author", "reader")
@login_required
def toggle_like(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    liked = Likes.query.filter_by(user_id=current_user.id, blog_id=blog.id).first()
    
    if liked:
        db.session.delete(liked)
        db.session.commit()
        flash("Unliked the Blog", "info")
    else:
        new_like = Likes(user_id=current_user.id, blog_id=blog.id)
        db.session.add(new_like)
        db.session.commit()
        flash("Liked the Blog", "success")
        
    return redirect(url_for("blog.view_blog", blog_id=blog.id))
        
    

@blog_bp.route("/created_blogs")
@roles_required("admin", "author")
@login_required
def show_created_blogs():
    all_blogs = current_user.blogs.all()
    return render_template("blog/created_blogs.html", all_blogs=all_blogs, user=current_user)
    
    

UPLOAD_FOLDER = os.path.join("app", "static", "uploads")
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@blog_bp.route("/create", methods=["GET", "POST"])
@roles_required("admin", "author")
@login_required
def create_blog():
    if request.method == "POST":
        category_id = request.form.get("category")
        blog_title = request.form.get("title")
        blog_content = request.form.get("content")
        
        
        
        selected_category = BlogCategory.query.get(category_id)
        if selected_category:
            blog = Blog(user_id=current_user.id, 
                        category_id=selected_category.id,
                        content=blog_content,
                        title=blog_title)
            
            db.session.add(blog)
            db.session.commit()
            
            images = request.files.getlist("images")
            
            
            for image_file in images:
                if image_file and allowed_file(image_file.filename):
                    filename = secure_filename(image_file.filename)
                    image_path = os.path.join(UPLOAD_FOLDER, filename)
                    image_file.save(image_path)
                    
                    relative_path = os.path.join("uploads", filename).replace('\\', '/')
                    
                    db_image = Image(blog_id=blog.id, image_path=relative_path)
                    db.session.add(db_image)
            db.session.commit()
                
            
            return redirect(url_for("blog.show_created_blogs"))
            
    return render_template("blog/create_blog.html")