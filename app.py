from flask import Flask, render_template, request, jsonify
from spellchecker import SpellChecker
import os

app = Flask(__name__)

# 🔥 Initialize SpellChecker
spell = SpellChecker(distance=2)

# 🔥 Load large dictionary
if os.path.exists("words.txt"):
    spell.word_frequency.load_text_file("words.txt")

# 🔥 Boost important technical words (very important!)
important_words = [
    "python", "flask", "django", "numpy", "pandas",
    "javascript", "html", "css", "react", "node",
    "machine", "learning", "nlp", "artificial",
    "intelligence", "backend", "frontend",
    "database", "api", "github"
]

for word in important_words:
    spell.word_frequency.add(word, 100000)  # Very high frequency


@app.route("/")
def index():
    return render_template("index.html")


def smart_correct(word):
    """
    Smarter correction logic
    """

    if word in spell:
        return word

    candidates = spell.candidates(word)

    if not candidates:
        return word

    # Pick highest frequency candidate
    best = max(candidates, key=lambda w: spell.word_frequency[w])

    return best


@app.route("/correct", methods=["POST"])
def correct():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"corrected": ""})

    text = data["text"].strip().lower()

    if text == "":
        return jsonify({"corrected": ""})

    words = text.split()
    corrected_words = []

    for word in words:
        corrected_words.append(smart_correct(word))

    corrected_text = " ".join(corrected_words)

    return jsonify({"corrected": corrected_text})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)