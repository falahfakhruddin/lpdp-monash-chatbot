import os

from app import create_app
from openai import OpenAI
import utils.markdown as md
import utils.json as uj

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
