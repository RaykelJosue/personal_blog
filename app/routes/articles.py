from flask import Blueprint, render_template, request
import os
import json
from datetime import datetime

articles_bp = Blueprint("articles", __name__)

ARTICLES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "articles")

def parse_date(date_str):
    """Intenta convertir una cadena de fecha en un objeto datetime."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")  # Ajusta el formato según cómo guardes las fechas
    except (ValueError, TypeError):
        return datetime.min  # Fecha mínima para que los artículos sin fecha se ordenen al final

def load_articles():
    articles = []
    if not os.path.exists(ARTICLES_DIR):
        return articles

    for filename in os.listdir(ARTICLES_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(ARTICLES_DIR, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    article = json.load(f)
                    article["id"] = int(article["id"])  # Convertir a entero
                    articles.append(article)
            except Exception as e:
                print(f"Error en {filename}: {e}")

    # Ordenar por ID ASCENDENTE (más antiguo primero)
    articles.sort(key=lambda x: x["id"])  # <-- Sin reverse
    return articles

@articles_bp.route("/")
def home():
    page = request.args.get("page", 1, type=int)
    articles = load_articles()
    per_page = 5
    total_articles = len(articles)
    total_pages = (total_articles + per_page - 1) // per_page  # Calcula total de páginas

    start = (page - 1) * per_page
    end = start + per_page
    paginated_articles = articles[start:end]
    
    return render_template("home.html", 
                           articles=paginated_articles, 
                           page=page, 
                           total_articles=total_articles,
                           total_pages=total_pages)

@articles_bp.route("/article/<int:article_id>")
def article(article_id):
    articles = load_articles()
    article = next((a for a in articles if a.get("id") == article_id), None)
    if article is None:
        return "Artículo no encontrado", 404
    return render_template("article.html", article=article, all_articles=articles)
