from flask import Flask
from flask_cors import CORS


def create_app(client, handbook_info, models):
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    from app.routes import register_routes
    register_routes(app, client, handbook_info, models)

    return app
