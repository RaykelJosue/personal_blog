from flask import Flask
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Importa los Blueprints
from app.routes.admin import admin_bp
from app.routes.auth import auth_bp
from app.routes.articles import articles_bp

# Registra los Blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(articles_bp)
