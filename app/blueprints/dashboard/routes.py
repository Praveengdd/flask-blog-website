from flask import Blueprint, render_template, flash, get_flashed_messages
from flask_login import login_required, current_user
from app.utils.decorators import roles_required
from app.models.blog import Blog


dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
@login_required
@roles_required("admin", "author", "reader")
def dashboard():
    all_blogs = Blog.query.all()
    flash("Login successfull!!!", "success")
    return render_template("dashboard/dashboard.html", user=current_user, all_blogs=all_blogs)
