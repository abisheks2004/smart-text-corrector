from flask import Flask, render_template, request, jsonify
from corrector import correct_with_textblob, correct_with_symspell
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    corrected_output = ""
    if request.method == "POST":
        input_text = request.form.get("text", "").strip()
        method = request.form.get("method", "symspell")

        if "file" in request.files:
            file = request.files["file"]
            if file and file.filename.endswith(".txt"):
                filepath = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(filepath)
                with open(filepath, "r", encoding="utf-8") as f:
                    input_text = f.read().strip()

        if input_text:
            if method == "textblob":
                corrected_text, summary = correct_with_textblob(input_text)
            else:
                corrected_text, summary = correct_with_symspell(input_text)

            corrected_output = (
                f"<h4>Wrong → Correct:</h4><p>{summary}</p>"
                f"<hr><h4>Corrected Text:</h4><p>{corrected_text}</p>"
            )
    return render_template("index.html", corrected=corrected_output)

@app.route("/live-correct", methods=["POST"])
def live_correct():
    data = request.get_json()
    text = data.get("text", "").strip()
    method = data.get("method", "symspell")

    if not text:
        return jsonify({"corrected": "", "summary": ""})

    if method == "textblob":
        corrected_text, summary = correct_with_textblob(text)
    else:
        corrected_text, summary = correct_with_symspell(text)

    return jsonify({"corrected": corrected_text, "summary": summary})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
