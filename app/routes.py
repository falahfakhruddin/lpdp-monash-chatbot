from flask import request, jsonify

import numpy as np


def register_routes(app, client, handbook_info, models):
    @app.route("/api/query", methods=["POST"])
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
        dot_product = np.dot(embedding_array, q_embedding_array)
        similarity = dot_product / (np.linalg.norm(embedding_array) * np.linalg.norm(q_embedding_array))

        indices = np.argsort(similarity)[-10:][::-1]

        # Convert to list if needed
        index_list = indices.tolist()
        information = "\n".join(f" - {handbook_info[i]}" for i in index_list)

        prompt = f"""
        Jawab pertanyaan berikut: {query_text}
        berdasarkan informasi berikut:
        {information}

        Hanya Jawab berdasarkan informasi yang diberikan. Jika informasi yang ada tidak cukup untuk menjawab pertanyaan jawab anda tidak bisa menjawabnya.
        """

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "developer", "content": "Anda adalah asisten taat yang menjawab pernyataan terbatas pada informasi yang diberikan"},
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        response_text = f"Response: {completion.choices[0].message.content}"

        return jsonify({"message": response_text})