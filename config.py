import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'QW3rtY12345.'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    ARTICLES_DIR = os.path.join(BASE_DIR, 'articles')  # Mover artículos a esta carpeta
    WTF_CSRF_ENABLED = True  

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
