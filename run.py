import os

from app import create_app
from openai import OpenAI
import utils.markdown as md
import utils.json as uj

open_ai_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=open_ai_key)

handbook_info = md.retrieve_data('handbook_extracted.md')
models = uj.load_json('embedding_model.json')
app = create_app(client, handbook_info, models)

if __name__ == "__main__":
    app.run(debug=True)
