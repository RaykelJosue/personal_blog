from flask import Blueprint, render_template, request, redirect, url_for, abort, session
import os
import json
import pytz
from datetime import datetime
from ..utils.articles import get_next_article_id  # <-- Importar la función

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

ARTICLES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "articles")

# Verifica si el usuario está logueado antes de acceder a cualquier ruta de admin
@admin_bp.before_request
def require_login():
    if not session.get("logged_in"):
        # Si no está logueado, redirige a /login
        return redirect(url_for("auth.login"))

@admin_bp.route("/")
def admin_dashboard():
    articles = []
    if os.path.exists(ARTICLES_DIR):
        for filename in os.listdir(ARTICLES_DIR):
            if filename.endswith(".json"):
                filepath = os.path.join(ARTICLES_DIR, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        articles.append(json.load(f))
                except (json.JSONDecodeError, IOError):
                    print(f"Error al leer el archivo {filename}")
    return render_template("admin_dashboard.html", articles=articles)

@admin_bp.route("/new", methods=["GET", "POST"])
def new_article():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]


        caracas_tz = pytz.timezone("America/Caracas")  
        now = datetime.now(caracas_tz)
        formatted_date = now.strftime("%d-%m-%Y %H:%M:%S")


        # Generar un ID numérico usando la función de utils/articles.py
        article_id = get_next_article_id()  # <-- ID numérico
        article = {
            "id": article_id,  # <-- ID numérico
            "title": title,
            "content": content,
            "date": formatted_date
        }
        os.makedirs(ARTICLES_DIR, exist_ok=True)
        filepath = os.path.join(ARTICLES_DIR, f"{article_id}.json")  # <-- Nombre del archivo con ID numérico
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(article, f, ensure_ascii=False, indent=4)
        return redirect(url_for("admin.admin_dashboard"))
    return render_template("new_article.html")


@admin_bp.route("/edit/<article_id>", methods=["GET", "POST"])
def edit_article(article_id):
    # Buscar el artículo a editar
    filepath = os.path.join(ARTICLES_DIR, f"{article_id}.json")
    if not os.path.exists(filepath):
        abort(404)  # Si el archivo no existe, muestra un error 404

    with open(filepath, "r", encoding="utf-8") as f:
        article = json.load(f)

    if request.method == "POST":
        # Obtener los nuevos datos del artículo desde el formulario
        article["title"] = request.form["title"]
        article["content"] = request.form["content"]
        article["date"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        caracas_tz = pytz.timezone("America/Caracas")  
        now = datetime.now(caracas_tz)


        formatted_date = now.strftime("%d-%m-%Y %H:%M:%S")
        article["date"] = formatted_date

        # Guardar los cambios en el archivo
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(article, f, ensure_ascii=False, indent=4)

        # Redirigir a la página de administración
        return redirect(url_for("admin.admin_dashboard"))

    return render_template("edit_article.html", article=article)

@admin_bp.route("/delete/<article_id>", methods=["POST"])
def delete_article(article_id):
    filepath = os.path.join(ARTICLES_DIR, f"{article_id}.json")
    if os.path.exists(filepath):
        os.remove(filepath)  # Elimina el archivo del artículo
        return redirect(url_for("admin.admin_dashboard"))  # Redirige al panel de administración
    else:
        return "Artículo no encontrado", 404


def load_articles():
    articles = []
    if os.path.exists(ARTICLES_DIR):
        for filename in os.listdir(ARTICLES_DIR):
            if filename.endswith(".json"):
                filepath = os.path.join(ARTICLES_DIR, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        article = json.load(f)
                        article["id"] = int(article["id"])  # <-- Convertir ID a entero
                        articles.append(article)
                except (json.JSONDecodeError, IOError, ValueError):
                    print(f"Error al leer el archivo {filename}")
    # Ordenar por ID ascendente
    articles.sort(key=lambda x: x["id"])  # <-- Ordenar por ID numérico
    return articles

@admin_bp.route("/view_article/<int:article_id>")
def view_article(article_id):
    articles = load_articles()
    article = next((a for a in articles if a.get("id") == article_id), None)
    if article is None:
        return "Artículo no encontrado", 404
    return render_template("admin_view_article.html", article=article)
