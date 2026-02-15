from flask import Flask, render_template, request, jsonify
from difflib import get_close_matches
import os

app = Flask(__name__)

# ✅ Absolute path for words.txt
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORDS_FILE = os.path.join(BASE_DIR, "words.txt")

# Load words from words.txt
def load_words():
    try:
        with open(WORDS_FILE, "r", encoding="utf-8") as f:
            return [line.strip().lower() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print("❌ words.txt file not found at:", WORDS_FILE)
        return []

word_list = load_words()

print("✅ Total words loaded:", len(word_list))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/correct", methods=["POST"])
def correct():
    data = request.get_json()

    if not data or "word" not in data:
        return jsonify({
            "best_correction": "No word received!",
            "suggestions": []
        })

    word = data["word"].strip().lower()

    if word == "":
        return jsonify({
            "best_correction": "Please type a word!",
            "suggestions": []
        })

    suggestions = get_close_matches(word, word_list, n=5, cutoff=0.6)
    best = suggestions[0] if suggestions else "No correction found"

    return jsonify({
        "best_correction": best,
        "suggestions": suggestions
    })




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



