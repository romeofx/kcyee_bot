from flask import Flask
import os


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
    app.config['DEBUG'] = True  # 👈 Add this line

    from .routes import main
    app.register_blueprint(main)

    return app

