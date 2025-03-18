from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import timedelta

auth_bp = Blueprint("auth", __name__)

# Datos de usuario "hardcodeados" (en producción se usaría una BD o variables de entorno)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "secret"

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            # Autenticación exitosa
            session["logged_in"] = True
            # Opcional: establecer duración de la sesión
            session.permanent = True
            # Redirigir al panel de administración
            return redirect(url_for("admin.admin_dashboard"))
        else:
            return render_template("login.html", error="Usuario o contraseña incorrectos")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("auth.login"))
