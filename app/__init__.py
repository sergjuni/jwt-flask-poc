from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from config import Config
from .routes import auth_bp

jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    jwt.init_app(app)

    app.register_blueprint(auth_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app