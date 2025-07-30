from flask import Blueprint, render_template, request, url_for, flash, get_flashed_messages, redirect
from app import db
from app.models.user import User
from app.models.role import Role
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
     if request.method == "POST":
          email = request.form.get("email").strip()
          password = request.form.get("password")
          
          user = User.query.filter_by(email=email).first()
          if user:
               if user.check_password(password):
                    login_user(user)
                    return redirect(url_for("dashboard.dashboard"))
               else:
                    flash("Wrong password!!!", "warning")
                    return redirect(url_for("auth.login"))
          else:
               flash("User not exists in the database!!!!", "warning")
               return redirect(url_for("auth.login"))
          
     return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
     if request.method == "POST":
          first_name = request.form.get("first_name").strip()
          last_name = request.form.get("last_name").strip()
          email = request.form.get("email").strip()
          password = request.form.get("password")
          role_id = request.form.get("role")
          
          if User.query.filter_by(email=email).first():
               flash("User with this email already exists!!!!", "warning")
               return redirect(url_for("auth.register"))
          
          
          new_user = User(first_name=first_name, last_name=last_name, email=email)
          new_user.set_password(password)
          selected_role = Role.query.get(role_id)
          if selected_role:
               new_user.roles.append(selected_role)
          db.session.add(new_user)
          db.session.commit()
          flash("Regirstration successfull!!! Login to your account!!!", "success")
          return redirect(url_for("auth.login"))
          
     return render_template("auth/register.html")


@auth_bp.route("/logout")
@login_required
def logout():
     logout_user()
     flash("Logged out sucessfully from your account!!!", "success")
     return redirect(url_for("auth.login"))

@auth_bp.route("/")
def home():
     return render_template("base.html")