from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from apikey import api_data
import speech_recognition as sr
import os

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=api_data)
MODEL = "gpt-4o"

# Route to process text commands
@app.route("/api/text", methods=["POST"])
def process_text():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        answer = completion.choices[0].message.content
        return jsonify({"reply": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Optional route to process uploaded audio using Python SR
@app.route("/api/audio", methods=["POST"])
def process_audio():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(file) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"transcript": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
