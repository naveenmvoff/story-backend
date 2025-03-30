from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from transformers import pipeline
from googletrans import Translator
from dotenv import load_dotenv
import audio  # Changed from backend.audio to just audio since they're in the same directory

# Load environment variables 
load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

# Add this new route to serve audio files
@app.route('/static/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory('static/audio', filename)

generator = pipeline("text-generation", model="gpt2")
translator = Translator()

# ✅ Function to Translate to Tamil
def translate_to_tamil(text):
    translated = translator.translate(text, dest="ta")
    return translated.text

@app.route("/generate-story", methods=["POST"])
def generate_story_endpoint():
    data = request.json
    prompt = data.get("prompt", "Genererate story(atlest 200 words) based on the word,  Note: Don't Generate unwanted content(sexulal, abuse, and other)")
    # story_in_english = generator(prompt, max_length=500, temperature=0.9)[0]["generated_text"]
    story_in_english = generator(
    prompt,
    max_length=700,  # Increase length for better depth
    temperature=0.7,  # Reduce randomness
    top_p=0.9,  # Keep diverse outputs
    top_k=50,  # Limit vocabulary selection
    repetition_penalty=1.2  # Avoid repetitive words
    )[0]["generated_text"]

    story_in_tamil = translate_to_tamil(story_in_english)

    print("Story generated Success")
    return jsonify({"english_story": story_in_english, "tamil_story": story_in_tamil})

@app.route("/generate-audio", methods=["POST"])
def generate_audio_endpoint():
    print("A - step 1")
    data = request.json
    print("A - step 2")
    text = data.get("text", "")
    language = data.get("language", "ta")  # Default to Tamil if not specified
    print("A - step 3")
    if not text.strip():
        print("A - step 3 - error")
        return jsonify({"error": "No text provided"}), 400
    
    print("A - step 4")
    audio_url = audio.generate_audio(text, language)
    print("A - step 5")
    if "error" in audio_url:
        print("A - step 5 - error")
        return jsonify({"error": audio_url["error"]}), 500
    
    print("A - step 6")
    return jsonify({"audio_url": audio_url})

if __name__ == "__main__":
    print("A - step 7")
    app.run(debug=True, port=5001)
