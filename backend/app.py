from openai import OpenAI
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.json
    prompt = data.get("prompt")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
