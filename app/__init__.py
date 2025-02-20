from flask import Flask
from flask_cors import CORS

from openai import OpenAI
import utils.markdown as md
import utils.json as uj
import os


def create_app():
    open_ai_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=open_ai_key)

    handbook_info = md.retrieve_data('handbook_extracted.md')
    models = uj.load_json('embedding_model.json')

    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    from app.routes import register_routes
    register_routes(app, client, handbook_info, models)

    return app
