from flask import request, jsonify

import numpy as np


def register_routes(app, client, handbook_info, models):
    @app.route("/query", methods=["POST"])
    def query():
        data = request.get_json()
        query_text = data.get("query", "")

        if not query_text:
            return jsonify({"error": "Query cannot be empty"}), 400

        # Simulate a response
        response = client.embeddings.create(
            input=query_text,
            model="text-embedding-3-small"
        )
        embedding_array = np.array(models)
        q_embedding = response.data[0].embedding
        q_embedding_array = np.array(q_embedding)
        similarity = 1 - np.dot(embedding_array, q_embedding_array)

        # Define threshold
        threshold = 0.45

        # Get indices where values are above the threshold
        indices = np.where(similarity < threshold)[0]
        if indices.shape[0] > 10:
            indices = np.argsort(similarity)[:10]

        # Convert to list if needed
        index_list = indices.tolist()
        information = "\n".join(f" - {handbook_info[i]}" for i in index_list)

        prompt = f"""
        Jawab pertanyaan berikut: {query_text}
        dengan mamanfaatkan informasi berikut:
        {information}


        """

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "developer", "content": "You are a helpful assistant. Jawab berdasarkan informasi yang diberikan. Jangan menjawab dari informasi internal model"},
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        response_text = f"Response: {completion.choices[0].message.content}"

        return jsonify({"message": response_text})