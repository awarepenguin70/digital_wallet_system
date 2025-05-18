from flask import Flask, url_for, redirect
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    from .blueprints.auth import auth_bp
    from .blueprints.transactions import transactions_bp
    from .blueprints.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(admin_bp)

    @app.route('/')
    def home():
        return redirect(url_for('auth.login'))

    return app