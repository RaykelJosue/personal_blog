import os
import json
import re
from flask import current_app

def get_articles_dir():
    return current_app.config.get("ARTICLES_DIR")

def extract_number(text):
    """Extrae un número del nombre del archivo JSON."""
    match = re.search(r'\d+', text)
    return int(match.group()) if match else 0

def get_next_article_id():
    """Obtiene el siguiente ID disponible basado en los archivos existentes."""
    articles_dir = get_articles_dir()
    if not os.path.exists(articles_dir):
        return 1  # Si no hay artículos, el primer ID será 1

    existing_ids = []
    for filename in os.listdir(articles_dir):
        if filename.endswith(".json"):
            try:
                # Extraer el ID del nombre del archivo (ej: "1.json" → 1)
                article_id = int(filename.split(".")[0])
                existing_ids.append(article_id)
            except ValueError:
                continue  # Ignorar archivos con nombres no válidos

    return max(existing_ids, default=0) + 1  # Siguiente ID disponible


def load_articles():
    articles = []
    articles_dir = get_articles_dir()
    
    if os.path.exists(articles_dir):
        for filename in os.listdir(articles_dir):
            if filename.endswith(".json"):
                with open(os.path.join(articles_dir, filename), "r", encoding="utf-8") as f:
                    articles.append(json.load(f))
    
    # Ordenar por ID ascendente
    articles.sort(key=lambda x: int(x['id']))
    
    return articles

def load_article(article_id):
    articles_dir = get_articles_dir()
    filepath = os.path.join(articles_dir, f"{article_id}.json")
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_article(article):
    articles_dir = get_articles_dir()
    os.makedirs(articles_dir, exist_ok=True)

    # Obtener el próximo ID disponible y asignarlo como número entero
    article['id'] = get_next_article_id()  # <-- Esto ya devuelve un número entero
    article['id'] = int(article['id'])  # <-- Asegurar que sea entero

    # Guardar el archivo con el ID numérico
    filepath = os.path.join(articles_dir, f"{article['id']}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(article, f, ensure_ascii=False, indent=4)


def delete_article(article_id):
    articles_dir = get_articles_dir()
    filepath = os.path.join(articles_dir, f"{article_id}.json")
    if os.path.exists(filepath):
        os.remove(filepath)
